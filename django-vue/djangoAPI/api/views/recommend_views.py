from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from django.http import JsonResponse
from rest_framework.response import Response
from django.core.cache import cache
from django.contrib import auth
from django.db.models import Max

from api.serializers import MovieSerializer
from api.models import create_profile
from api.models import User, Profile, Movie, Rating, UserCluster

from api.algorithms.kmeansClustering import U_Cluster

import scipy.sparse as sp
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from collections import Counter

import pandas as pd
import numpy as np
import json
import time
import os
import random

BASE_DIR = os.path.dirname(
            os.path.dirname(
                    os.path.dirname(
                            os.path.abspath(__file__)
                    )
            )
        )

url = os.path.join(BASE_DIR, 'data')
latent_user = np.load(os.path.join(url, 'mapper/latent_user.npy'))
latent_movie = np.load(os.path.join(url, 'mapper/latent_movie.npy'))
user_mapper = open(os.path.join(url, 'mapper/userMapper.json')).read()
user_mapper = json.loads(user_mapper)
movie_mapper = open(os.path.join(url, 'mapper/movieMapper.json')).read()
movie_mapper = json.loads(movie_mapper)
link = pd.read_csv(os.path.join(url, 'the-movies-dataset/links.csv'))
cluster_movie_list = open(os.path.join(url, 'movie_list.json')).read()
cluster_movie_list = json.loads(cluster_movie_list)
cluster_movie_list_v2 = open(os.path.join(url, 'movie_list_v2.json')).read()
cluster_movie_list_v2 = json.loads(cluster_movie_list_v2)
df_keys = pd.read_csv('df_keys.csv')
cv_mx = CountVectorizer().fit_transform(df_keys['keywords'])

# 추천 시스템
# 앞으로 가입할 새로운 유저: 기존 유저 kmeans 이용해 앞으로 가입할 새로운 유저 군집에 할당(정보가 없는 새로운 유저에게 영화 추천 어려움이 있기 때문에 기존의 27만명의 유저 kmeans 군집 정보 이용해 새로운 유저를 가까운 군집 특성에 맞춰 추천해주려고)
# kMeans 군집화는 앞으로 주기적으로 할 예정.

# Hybrid filtering(Switching 사용)
# 유저가 평가한 영화 수 20개 이상일 때,
# Collaborative filtering
# 유저가 평가한 영화 수 20개 미만일 때,
# Content based filtering/ topN개에서 몇 개(ex.3)만 뽑아서 content based에 넣어서 추천.

# => 필요한 정보: 유저별 평가한 영화 개수


def get_ratingNum(userid):
    user = User.objects.get(id=userid)
    ratings = Rating.objects.filter(user__id=userid)
    rating_num = len(ratings)
    return rating_num

def get_movie_list(df_keys, datas):

    movie_list = []
    for index in datas.index:
        movie_list.append(Movie.objects.get(pk=df_keys.iloc[index]['id']))
    return movie_list

def recommend_movie(df_keys, indices, id, cosine_sim, n):

    movies = []

    # 일치하는 영화가 있는지 검사합니다.
    if id not in indices.index:
        print("Movie not in database.")
        return

    # 내림차순으로, Cosine Simirality을 정렬합니다.
    scores = pd.Series(cosine_sim[0]).sort_values(ascending = False)
    print(scores)

    # 가장 유사한 n(10)개만 추출합니다.
    # 첫번째 index의 영화의 경우 활성화된 영화와 같기 때문에 제외합니다.
    top_n_idx = list(scores.iloc[1:n].index)

    # 타이틀을 기준으로 추출합니다.
    return df_keys['title'].iloc[top_n_idx]

def collaborative_filtering(user, movies):
    # 1. 해당 유저의 예측 평점
    # user vector
    user_map = user_mapper[str(user.id)]
    user_vec = latent_user[user_map]

    predict_ratings = {}
    # movie vector
    for movie in movies:
        tmdb_id = movie[0]
        if movie[1] != 'nan':
            imdb_id = int(movie[1][2:])
        else:
            imdb_id = None
        try:
            movieId = None
            try:
                movieId = int(link[link['tmdbId'] == tmdb_id]['movieId'])
            except TypeError:
                if imdb_id == None:
                    continue
                else:
                    movieId = int(link[(link["imdbId"] == imdb_id) & (link["tmdbId"] == tmdb_id)]['movieId'])
            movie_map = movie_mapper[str(movieId)]
            movie_vec = latent_movie[movie_map]
            # 예측 평점
            predict = np.dot(user_vec, movie_vec.T)
            predict_ratings[tmdb_id] = predict
        except KeyError:
            continue

    # 2. 예측 평점 topN movie
    movie_list = []
    rating_desc = sorted(predict_ratings.items(), key=lambda t: t[1], reverse=True)

    topN = 20
    if len(rating_desc) > topN:
        rating_desc = rating_desc[:topN]
    movie_list = [movie[0] for movie in rating_desc]
    print(movie_list)
    return movie_list


@api_view(['GET'])
def RecommendMovie(request):
    start = time.time()
    topN = 20
    print(request.method)
    
    if request.method == 'GET':
        target_id = request.GET.get('id', request.GET.get('movie_id', None))

        if target_id is None:
            return JsonResponse({'msg': "Invalid Request Method", 'status': status.HTTP_400_BAD_REQUEST})

        target_user = User.objects.get(id=target_id)
        # 유저가 매긴 평점 개수
        rating_num = get_ratingNum(target_id)
        # 기존 군집화 유무에 따른 군집 정보 가져오기
        max_id_object = UserCluster.objects.aggregate(user_id=Max('user_id'))
        max_id = max_id_object['user_id']

        # (1) 군집 할당 안 된 유저
        if int(target_id) > max_id:  # 군집 할당 안된 유저
            new_users = U_Cluster()  # 군집 할당 안된 모든 유저 목록
            target_user_df = new_users[new_users.index == int(target_id)]  # 해당 유저
            target_cluster = int(target_user_df['cluster'].values)
        # (2) kmeans 클러스터링 반영 된 유저
        else:
            target_cluster = target_user.profile.kmeans_cluster

        movie_list = []
        movies = None
        # 1. 유저가 매긴 평점 개수가 20개 이상인 경우 collaborative filtering
        if rating_num >= 20:

            # 1. 해당 유저가 본 영화
            user_watched = [[rating.movie.id, rating.movie.imdb_id] for rating in Rating.objects.filter(user__id=target_id)]

            # 2. 해당 군집 유저들이 본 모든 영화

            # ================= 속도 개선 버전(파일 있을 때만 가능) =================== #
            movie_list = cluster_movie_list_v2[0][str(target_cluster)]
            # 해당 유저가 본 영화 제외
            movies = filter(lambda x: x not in user_watched, movie_list)

            movie_list = collaborative_filtering(target_user, movies)
            movies = Movie.objects.filter(id__in=movie_list)
            # ================= 속도 개선 버전(파일 있을 때만 가능) =================== #

            # =================기존 버전 =================== #
            # cluster_users = Profile.objects.filter(kmeans_cluster=target_cluster)
            # cluster_users_list = [user.id for user in cluster_users]

            # movies = []
            # ratings = Rating.objects.filter(user__id__in=cluster_users_list).exclude(user__id=target_id)

            # # 해당 유저가 본 영화 제외
            # movies = [(rating.movie.id, rating.movie.imdb_id) for rating in ratings if rating.movie.id not in user_watched]

            # 중복제거
            # movies = list(set(movies))
            # =================기존 버전 =================== #

        # 2. 유저가 매긴 평점 개수가 20개 미만인 경우 content based filtering
        else:
            print('평점개수 20개 미만')
            # 2-1. 0인 경우 따로 빼서 -> kmeans 안되있는경우 가져오고. (신규 유저)
            if rating_num == 0:  # 신규 유저
                print('rating 0개')
                # 2-1-2. 해당 군집 movie_list
                # (1) 해당 군집 모든 유저
                # ================= 속도 개선 버전(파일 있을 때만 가능) =================== #
                movie_list = cluster_movie_list[0][str(target_cluster)]

                movie_list = random.sample(movie_list, 20)

                movies = Movie.objects.filter(id__in=movie_list)
                # ================= 속도 개선 버전(파일 있을 때만 가능) =================== #

                # ================= 기존 버전 =================== #
                # cluster_users = Profile.objects.filter(kmeans_cluster=target_cluster)
                # cluster_users_list = [user.id for user in cluster_users]

                # for i, user in enumerate(cluster_users_list):
                #     print(i)
                #     ratings = Rating.objects.filter(user__id=user)
                #     movie_list += [rating.movie.id for rating in ratings]

                # movie_list = random.sample(movie_list, 5)

                # movies = Movie.objects.filter(id__in=movie_list)
                # ================= 기존 버전 =================== #


            # 2-2. rating이 조금이라도 있는 경우, 해당 유저가 본 영화 list 추출
            else:

                ratings = Rating.objects.filter(user__id=target_id)
                movie_list = [rating.movie.id for rating in ratings]
                if len(movie_list) >= 20:
                    movie_list = random.sample(movie_list, 20)

                content_based_movies = []
                print(movie_list)
                for movie_id in movie_list:
                    selectedMovie = df_keys.loc[df_keys['id'] == movie_id]
                    # selectedMovie = df_keys.loc[df_keys['id'] == 862]
                    idx = str(selectedMovie['Unnamed: 0']).split(' ')
                    idx = int(idx[0])
                    content_based_movies.append(cv_mx[idx:idx + 1])
                
                sum_vector = []
                for movie_vector in content_based_movies:
                    print(movie_vector.toarray())
                    if len(sum_vector) == 0:
                        sum_vector = movie_vector.toarray()    
                    sum_vector += movie_vector.toarray()

                print(sum_vector)
                
                cosine_sim = cosine_similarity(sp.csr_matrix(sum_vector), cv_mx)
                indices = pd.Series(df_keys.index, index = df_keys['id'])

                serializer = MovieSerializer(get_movie_list(df_keys, recommend_movie(df_keys, indices, movie_list[0], cosine_sim, 50)), many=True)
                return JsonResponse({'status': status.HTTP_200_OK, 'result': serializer.data}, safe=False)

        serializer = MovieSerializer(movies, many=True)
        return JsonResponse({'status': status.HTTP_200_OK, 'result': serializer.data}, safe=False)
