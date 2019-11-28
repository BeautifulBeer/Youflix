from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Movie, Rating, User, Crew, Cast, UserCluster
from api.algorithms.kmeansClustering import U_Cluster
# from django.contrib.auth.models import User
from api.serializers import MovieSerializer,MovieAgeSerializer,MovieGenderSerializer
from rest_framework.response import Response
from django.http import JsonResponse

# Django Database Model
from django.db.models import F

import json
import operator

import re
import os
import math
import time
import csv
import datetime
from django.core.cache import cache

from django.db.models import F
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import sklearn.preprocessing as pp

import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
from django.conf import settings

from ast import literal_eval
from rake_nltk import Rake
from scipy import sparse

# Caching
from django.http import JsonResponse
from django.core.cache import cache

from scipy import sparse
import sklearn.preprocessing as pp

# Numba
from numba import jit, prange
from numba import types, typeof
from numba.typed import Dict


@api_view(['GET'])
def algorithm(request):
    """
        Content-Based Algorithm
    """
    if request.method == 'GET':

        email = request.GET.get('email', None)
        page = request.GET.get('page', 1)
        feature = request.GET.get('feature', None)

        if email is None:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})

        user = User.objects.get(email=email)
        page = int(page)

        user = User.objects.get(email=email)
        ratings = Rating.objects.filter(user=user)
        rating_count = len(ratings)

        # 평가한 영화가 하나도 없다면 최신 영화를 추천해줍니다.
        if len(ratings) == 0:
            movies = Movie.objects.all()
            movies = movies.order_by(F('release_date').desc(nulls_first=False))
            movies = movies[(50 * (page - 1)): (50 * page)]
        else:

            # Read preprocessing data
            if feature == 'Director':
                df_keys = pd.read_csv('df_keys_crew.csv')
            elif feature == 'Actor':
                df_keys = pd.read_csv('df_keys_cast.csv')
            elif feature == 'Director/Actor':
                df_keys = pd.read_csv('df_keys_crew_cast.csv')
            else:
                df_keys = pd.read_csv('df_keys.csv')

            # All Movies Vectorizer
            # scikit-learn의 TF-IDF Vectorizer 사용하여 키워드를 토큰화하여 행렬을 분석하여 각 단어의 빈도를 분석합니다.
            tfidf_vectorizer = TfidfVectorizer()
            tf_mx = tfidf_vectorizer.fit_transform(df_keys['keywords'])
            features_len = len(tfidf_vectorizer.get_feature_names())

            # 영화에 대한 유사도 값을 저장할 배열입니다.
            selected_movies = [[0 for i in range(features_len)]]

            # 평가한 영화를 제외하기 위한 Set 입니다.
            seen_movie_set = set()

            for user_rating in ratings:
                seen_movie_set.add(user_rating.movie.id)
                movie_frame = df_keys.loc[df_keys['id'] == user_rating.movie.id]
                
                idx = int(str(movie_frame['Unnamed: 0']).split(' ')[0])
                movie = tf_mx[idx: idx + 1]

                col = movie.tocoo().col

                for index in range(len(col)):
                    selected_movies[0][col[index]] += 1 * math.exp(user_rating.rating)

            # Cosine Similarity 알고리즘을 사용하여 유사도를 분석합니다.
            cosine_sim = linear_kernel(selected_movies, tf_mx)

            # 일치하는 index list를 생성합니다.
            indices = pd.Series(df_keys.index, index=df_keys['id'])

            # 유사도 높은 순으로 n개의 추천 영화를 추출합니다.
            n_rank_list = recommend_movie(df_keys, indices, cosine_sim, -1)
            n_rank_list = n_rank_list[(50 * (page - 1)): (50 * page)]
            movies = []

            for movie_idx in n_rank_list:
                if movie_idx in seen_movie_set:
                    continue
                movies.append(Movie.objects.get(id=movie_idx))
        serializer = MovieSerializer(movies, many=True)
        return JsonResponse({'status': status.HTTP_200_OK, 'result': serializer.data, 'msg': rating_count }, safe=False)


@api_view(['GET'])
def preprocessing_for_cb(request):
    
    # DB에서 모든 movie 정보를 가져옵니다.
    movies = Movie.objects.all()
    # movies 객체를 DataFrame화 합니다.
    movies_frame = pd.DataFrame(movies.values())

    # 불필요한 Column들을 Drop 해줍니다.
    movies_frame = movies_frame.drop('imdb_id', axis=1)
    movies_frame = movies_frame.drop('adult', axis=1)
    movies_frame = movies_frame.drop('collection_id', axis=1)
    movies_frame = movies_frame.drop('budget', axis=1)
    movies_frame = movies_frame.drop('homepage', axis=1)
    movies_frame = movies_frame.drop('popularity', axis=1)
    movies_frame = movies_frame.drop('poster_path', axis=1)
    movies_frame = movies_frame.drop('backdrop_path', axis=1)
    movies_frame = movies_frame.drop('revenue', axis=1)
    movies_frame = movies_frame.drop('runtime', axis=1)
    movies_frame = movies_frame.drop('status', axis=1)
    movies_frame = movies_frame.drop('tagline', axis=1)
    movies_frame = movies_frame.drop('video', axis=1)
    movies_frame = movies_frame.drop('vote_average', axis=1)
    movies_frame = movies_frame.drop('vote_count', axis=1)
    movies_frame = movies_frame.drop('release_date', axis=1)

    # 각 영화에 대한 Keyword와 Genre를 추출합니다.
    keywords = []
    genres = []
    crews_list = []
    casts_list = []

    # DataFrame을 하나씩 참조하며 해당 영화에 맞는 Keyword와 Genre들을 저장합니다.
    # 없을 경우 ''을 삽입 합니다.
    for element in movies_frame.values:

        # id를 통해 movie 객체를 가져와서 필요한 정보를 추출합니다.
        movie = Movie.objects.get(id=element[0])
        
        # 감독과 배우 정보를 가져옵니다.
        crews = Crew.objects.filter(movie=movie)
        casts = Cast.objects.filter(movie=movie)

        if len(crews) == 0:
            crews_list.append('')
        else:
            temp = []
            for crew in crews:
                if crew.job == 'Director':
                    temp.append(crew.name)
                    break
            if len(temp) == 0:
                crews_list.append('')
            else:
                crews_list.append(temp)

        if len(casts) == 0:
            casts_list.append('')
        else:
            temp = []
            for cast in casts:
                temp.append(cast.name)
                if len(temp) == 3:
                    break
            casts_list.append(temp)
        
        if len(movie.keywords.all()) is not 0:

            temp = []

            for keyword in movie.keywords.all():
                temp.append(keyword.name)
            keywords.append(temp)
        else:
            keywords.append('')

        if len(movie.genres.all()) is not 0:

            temp = []

            for genre in movie.genres.all():
                temp.append(genre.name)
            genres.append(temp)
        else:
            genres.append('')

    # test
    # pd.set_option('display.max_columns', 30)

    # 데이터 전처리 및 생성
    movies_frame['crews'] = ''
    movies_frame['casts'] = ''
    # 1. overview가 없는 영화에 대해서 ''로 모두 할당 해줍니다.
    movies_frame['overview'] = movies_frame['overview'].fillna('')
    # 2. Genre 데이터를 삽입합니다.
    movies_frame = movies_frame.assign(genres=genres)
    # 3. Keyword 데이터를 삽입합니다.
    movies_frame = movies_frame.assign(keywords=keywords)
    # 4. Crew 데이터를 삽입합니다.
    movies_frame = movies_frame.assign(crews=crews_list)
    # 5. Cast 데이터를 삽입합니다.
    movies_frame = movies_frame.assign(casts=casts_list)

    # genres, keywords 데이터에 대해서 공백(' ')을 없애줍니다.
    movies_frame['genres'] = movies_frame['genres'].apply(preprocessing_genres)
    movies_frame['keywords'] = movies_frame['keywords'].apply(preprocessing_keyword)

    # Rake(Rapid Automatic Keyword Extraction)을 이용해서 줄거리에 대한 keyword을 추출합니다.
    movies_frame['overview'] = movies_frame['overview'].apply(preprocessing_overview)


    # 앞에서 만든 데이터를 통하여 새로운 DataFrame을 생성합니다.
    df_keys = pd.DataFrame()
    df_keys['title'] = movies_frame['title']
    df_keys['keywords'] = ''
    df_keys['id'] = movies_frame['id']

    # 만들어진 단어들을 하나의 단어 모음으로 만듭니다.
    df_keys['keywords'] = movies_frame.apply(bag_words, axis=1)

    # 지금까지의 결과를 .csv 파일로 저장합니다.
    df_keys.to_csv('df_keys_crew_cast.csv', mode='w')

    # ============================== WARNING ==================================
    # 여기서 부터 아래의 코드를 실행하고 싶을 경우,
    # df_keys_*.csv 파일들 중 하나를 Pandas의 DataFrame으로 가져와야 합니다.
    # =========================================================================

    # scikit-learn의 CountVectorizer를 사용하여 키워드를 토큰화하여 행렬을 조사하여 각 단어의 빈도를 분석합니다.
    tfidf_vectorizer = TfidfVectorizer()
    tf_mx = tfidf_vectorizer.fit_transform(df_keys['keywords'])

    selected_movies = df_keys.loc[df_keys['id'] == 862]
    idx = str(selectedMovie['Unnamed: 0']).split(' ')
    idx = int(idx[0])

    # Cosine Similarity 알고리즘을 사용하여 유사도를 분석합니다.
    cosine_sim = cosine_similarity(tf_mx[idx: idx+1], tf_mx)

    # 일치하는 index list를 생성합니다.
    indices = pd.Series(df_keys.index, index=df_keys['id'])

    # id 597에 대한 상위 10개의 추천 영화를 추출합니다.
    # print(recommend_movie(df_keys, indices, cosine_sim, 10))
    # print(test_recommend_movie(df_keys, 862, indices, 10, cosine_sim))
    return Response(status=status.HTTP_200_OK)

# def test_recommend_movie(df_keys, movie_id, indices, n, cosine_sim):
#     movies = []
#     # retrieve matching movie title index
#     if movie_id not in indices.index:
#         print("Movie not in database.")
#         return
#     else:
#         idx = indices[movie_id]
#     # cosine similarity scores of movies in descending order
#     scores = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
#     # top n most similar movies indexes
#     # use 1:n because 0 is the same movie entered
#     top_n_idx = list(scores.iloc[1:n].index)      
#     return df_keys['title'].iloc[top_n_idx]

def recommend_movie(df_keys, indices, cosine_sim, n):

    # 내림차순으로, Cosine Simirality을 정렬합니다.
    scores = pd.Series(cosine_sim[0]).sort_values(ascending=False)

    # 가장 유사한 n개만 추출합니다.
    # 첫번째 index의 영화의 경우 활성화된 영화와 같기 때문에 제외합니다.
    # * n이 -1이면 전체를 뜻합니다.

    if n == -1:
        top_n_idx = list(scores.iloc[1:].index)
    else:
        top_n_idx = list(scores.iloc[1:n].index)

    # Movie ID를 기준으로 추출합니다.
    return df_keys['id'].iloc[top_n_idx]


def preprocessing_keyword(data):

    ret = []
    for keyword in data:
        ret.append(keyword.replace(' ', ''))
    return ret


def preprocessing_genres(data):

    ret = []
    for genre in data:
        ret.append(genre.replace(' ', ''))
    return ret


def preprocessing_director(data):

    if data is np.NaN:
        return np.NaN
    ret = data.replace(' ', '')
    return ret


def preprocessing_overview(data):

    plot = data
    rake = Rake()
    rake.extract_keywords_from_text(plot)
    scores = rake.get_word_degrees()
    return(list(scores.keys()))


def bag_words(x):
    return (' '.join(x['genres']) + ' ' + ' '.join(x['keywords']) + ' ' + ' '.join(x['title']) + ' ' + ' '.join(x['overview']) + ' ' + ' '.join(x['crews']) + ' ' + ' '.join(x['casts']))
