from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from django.http import JsonResponse
from django.core.cache import cache
from django.contrib import auth
from django.db.models import Max

from api.serializers import ProfileSerializer, SessionSerializer
from api.serializers import RecommendMovie, SimilarUserSerializer
from api.models import create_profile
from api.models import User, Profile, Movie, Rating, UserCluster

from api.algorithms.kmeansClustering import U_Cluster

from collections import Counter

import pandas as pd
import numpy as np
import json
import time

# import logging
# logger = logging.getLogger("mylogger")

import os
BASE_DIR = os.path.dirname(
            os.path.dirname(
                    os.path.dirname(
                            os.path.abspath(__file__)
                    )
            )
        )


# 여러명의 사용자들을 가입시키는 Request
@api_view(['POST'])
def signup_many(request):
    if request.method == 'POST':
        profiles = request.data.get('profiles', None)
        for profile in profiles:
            userid = profile.get('userid', None)
            email = profile.get('email', None)
            username = profile.get('username', None)
            password = profile.get('password', None)
            age = profile.get('age', None)
            occupation = profile.get('occupation', None)
            gender = profile.get('gender', None)
            create_profile(
                    id=userid,
                    email=email,
                    username=username,
                    password=password,
                    age=age,
                    occupation=occupation,
                    gender=gender
                    )

        return JsonResponse({'status': status.HTTP_200_OK})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


# 다수의 사용자를 얻을 때 사용하는 Request
@api_view(['GET'])
def getUsers(request):
    if request.method == 'GET':
        age = request.GET.get('age', None)
        gender = request.GET.get('gender', None)
        occupation = request.GET.get('occupation', None)
        page = request.GET.get('page', 1)
        profiles = Profile.objects.all()
        if age:
            profiles = profiles.filter(age=age)
        if gender:
            profiles = profiles.filter(gender=gender)
        if occupation:
            profiles = profiles.filter(occupation=occupation)
        if page:
            page = int(page)
            if page <= len(profiles)//50+1:
                start = 50*(page-1)
                end = start+50
                if len(profiles[start:]) < 50:
                    profiles = profiles[start:]
                profiles = profiles[start:end]

        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse({
                'result': serializer.data,
                'status': status.HTTP_200_OK
                })
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


# 회원가입
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        params = request.data.get('params', None)
        email = params.get('email', None)
        username = params.get('username', None)
        password = params.get('password', None)
        age = params.get('age', None)
        gender = params.get('gender', None)
        occupation = params.get('occupation', None)
        genres = params.get('genres', None)

        if gender == 'female':
            gender = 'F'
        elif gender == 'male':
            gender = 'M'

        cluster_max_id_obj = UserCluster.objects.aggregate(user_id=Max('user_id'))
        profile_max_id_obj = Profile.objects.aggregate(user_id=Max('user_id'))
        if profile_max_id_obj['user_id'] < cluster_max_id_obj['user_id']:
            max_id = cluster_max_id_obj['user_id']
        else:
            max_id = profile_max_id_obj['user_id']

        try:
            create_profile(
                    id=max_id+1,
                    email=email,
                    username=username,
                    password=password,
                    age=age, occupation=occupation,
                    gender=gender,
                    movie_taste=genres
                    )
        except Exception:
            return JsonResponse({
                    'status':
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'msg': Exception
                    })
        return JsonResponse({'status': status.HTTP_200_OK})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        # 밑에 3줄은 딱히 필요없을 것 같다.
        if email is None or password is None:
            return JsonResponse({'msg': "Not input ID and Password", 'status': status.HTTP_400_BAD_REQUEST})
        if email is None:
            return JsonResponse({'msg': "Not input Email", 'status': status.HTTP_400_BAD_REQUEST})
        if password is None:
            return JsonResponse({'msg': "Not input Password", 'status': status.HTTP_400_BAD_REQUEST})

        user = auth.authenticate(email=email, password=password)

        if user:
            auth.login(request, user)
            # 토큰이 서버에서 아직 지워지지 않았거나, auth_token이 그대로 남아있으면 삭제한다
            if Token.objects.filter(user=user).first():
                if str(Token.objects.get(user=user)) in request.session.keys():
                    del request.session[str(Token.objects.get(user=user))]
                user.auth_token.delete()
            token = Token.objects.create(user=user)
            request.session[str(token)] = email
            profile = Profile.objects.get(user=user)
            result = {
                'email': email,
                'username': profile.username,
                'gender': profile.gender,
                'age': profile.age,
                'occupation': profile.occupation,
                'token': token,
                'is_staff': profile.user.is_staff,
                'is_auth': True,
                'movie_taste': profile.movie_taste
            }
        else:
            result = {
                'email': None,
                'username': None,
                'gender': None,
                'age': None,
                'occupation': None,
                'token': None,
                'is_staff': False,
                'is_auth': False,
                'movie_taste': None
            }
        serializer = SessionSerializer(result)
        return JsonResponse({
            'status': status.HTTP_200_OK,
            'result': serializer.data
        }, safe=False)
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        token = request.data.get('token', None)
        user = User.objects.get(email=request.session[str(token)])
        del request.session[str(token)]
        user.auth_token.delete()
        auth.logout(request)
        return JsonResponse({'status': status.HTTP_200_OK})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


@api_view(['DELETE'])
def deleteUser(request):
    if request.method == 'DELETE':
        id = request.GET.get('id', None)
        users = User.objects.all()
        user = users.get(id=id)
        user.delete()
        return JsonResponse({'status': status.HTTP_200_OK})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


@api_view(['POST'])
def updateUser(request):
    if request.method == 'POST':
        params = request.data.get('params', None)
        token = params.get('token', None)
        email = params.get('email', None)
        username = params.get('username', None)
        password = params.get('password', None)
        occupation = params.get('occupation', None)
        genres = params.get('genres', None)

        if token is None or email is None or username is None or password is None or occupation is None or genres is None:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})
        try:
            user = User.objects.get(email=email)
            del request.session[str(token)]
            user.auth_token.delete()
            auth.logout(request)

            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)
            user.set_password(password)
            user.save()

            movie_taste_ = []
            for genre in genres:
                movie_taste_.append(genre)

            profile.username = username
            profile.occupation = occupation
            profile.movie_taste = movie_taste_
            profile.save()

            user = auth.authenticate(email=email, password=password)
            auth.login(request, user)
            token = Token.objects.create(user=user)
            request.session[str(token)] = email

            result = {
                    'email': email,
                    'username': profile.username,
                    'gender': profile.gender,
                    'age': profile.age,
                    'occupation': profile.occupation,
                    'token': token,
                    'is_staff': profile.user.is_staff,
                    'is_auth': True,
                    'movie_taste': profile.movie_taste
            }
            serializer = SessionSerializer(result)
            return JsonResponse({'status': status.HTTP_200_OK, 'result': serializer.data})
        except KeyError as e:
            return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': f'Keyerror {e}'})
        except User.DoesNotExist as e:
            return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': f'DoesNotExists {e}'})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


@api_view(['GET'])
def similarUser(request):

    if request.method == 'GET':
        target_id = request.GET.get('id', None)

        if target_id:
            target_user = Profile.objects.get(id=target_id)
            target_cluster = target_user.kmeans_cluster
            similar_users = Profile.objects.filter(kmeans_cluster=target_cluster)
            similar_users = similar_users.exclude(id=target_id)

        serializer = SimilarUserSerializer(similar_users, many=True)
        return JsonResponse({
            'result': serializer.data,
            'status': status.HTTP_200_OK
            })
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


url = os.path.join(BASE_DIR, 'data', 'mapper')
latent_user = np.load(os.path.join(url, 'latent_user.npy'))
latent_movie = np.load(os.path.join(url, 'latent_movie.npy'))
user_mapper = open(os.path.join(url, 'userMapper.json')).read()
user_mapper = json.loads(user_mapper)
movie_mapper = open(os.path.join(url, 'movieMapper.json')).read()
movie_mapper = json.loads(movie_mapper)


@api_view(['GET'])
def RecommendMovieUserBased(request):
    start = time.time()
    topN = 20
    if request.method == 'GET':

        target_id = request.GET.get('id', None)
        if target_id:
            max_id_object = UserCluster.objects.aggregate(user_id=Max('user_id'))
            max_id = max_id_object['user_id']
            # 군집 할당 안된 새로운 유저에 대해
            if int(target_id) > max_id:
                new_users = U_Cluster()
                target_user_df = new_users[new_users.index == int(target_id)]
                target_cluster = int(target_user_df['cluster'].values)
                target_user = Profile.objects.get(id=target_id)
                print('START')
                # cache hit
                if cache.get(target_cluster, default=None) is not None:
                    print("cache HIT!!!")
                    start = time.time()
                    df = pd.DataFrame(cache.get(target_cluster))
                    print(time.time() - start)
                # cache miss
                else:
                    print("cache miss...")
                    start = time.time()
                    similar_users = Profile.objects.filter(kmeans_cluster=target_cluster)
                    similar_user_list = [user.id for user in similar_users]

                    # 2. 해당 군집 모든 유저가 가장 많이 시청한 영화
                    movie_list = []
                    for userid in similar_user_list:
                        ratings = Rating.objects.filter(user__id=userid)
                        for rating in ratings:
                            movie_list.append(rating.movie.id)

                    movie_counts = Counter(movie_list)
                    movie_dict = dict(movie_counts)
                    df = pd.DataFrame(list(movie_dict.items()), columns=['id', 'count'])
                    # 5개 미만의 평점수를 가진 영화 제거
                    df = df[df['count'] >= 5]
                    # 3. 많이 본 영화 내림차순 정렬
                    df = df.sort_values(["count"], ascending=[False])

                    # cache에 target_cluster를 key로하는 value를 삽입.
                    cache.set(target_cluster, df, None)
                    print(time.time() - start)

                # 4. 타켓유저가 보지 않은 영화들 중 재밌을 것 같은 영화 TopN 추천
                print(df)
                target_user_watched = [rating.movie.id for rating in target_user.user.rating_set.all()]
                topN_movies = []
                for idx in range(len(df)):
                    if df.iloc[idx].id not in target_user_watched:
                        topN_movies.append([df.iloc[idx].id, 0])
                topN_movies = topN_movies[:topN]
                print(topN_movies)
                movie_list = []
                for movie in topN_movies:
                    movie_list.append(movie[0])
                data = Movie.objects.filter(id__in=movie_list)
                print(data)

                serializer = RecommendMovie(data, many=True)
                return JsonResponse({'status': status.HTTP_200_OK, 'result': serializer.data}, safe=False)

            # 이미 군집에 할당된 유저에 대해
            else:
                # 1. target_id user와 같은 군집인 users
                target_user = Profile.objects.get(id=target_id)
                target_cluster = target_user.kmeans_cluster
                print('START')
                # cache hit
                if cache.get(target_cluster, default=None) is not None:
                    print("cache HIT!!!")
                    start = time.time()
                    df = pd.DataFrame(cache.get(target_cluster))
                    print(time.time() - start)
                # cache miss
                else:
                    print("cache miss...")
                    start = time.time()
                    similar_users = Profile.objects.filter(kmeans_cluster=target_cluster)
                    similar_user_list = [user.id for user in similar_users]

                    # 2. 해당 군집 모든 유저가 가장 많이 시청한 영화
                    movie_list = []
                    for userid in similar_user_list:
                        ratings = Rating.objects.filter(user__id=userid)
                        for rating in ratings:
                            movie_list.append(rating.movie.id)

                    movie_counts = Counter(movie_list)
                    movie_dict = dict(movie_counts)
                    df = pd.DataFrame(list(movie_dict.items()), columns=['id', 'count'])
                    # 5개 미만의 평점수를 가진 영화 제거
                    df = df[df['count'] >= 5]
                    # 3. 많이 본 영화 내림차순 정렬
                    df = df.sort_values(["count"], ascending=[False])

                    # cache에 target_cluster를 key로하는 value를 삽입.
                    cache.set(target_cluster, df, None)
                    print(time.time() - start)

                # 4. 타켓유저가 보지 않은 영화들 중 재밌을 것 같은 영화 TopN 추천
                target_user_watched = [rating.movie.id for rating in target_user.user.rating_set.all()]
                target_user_id = int(user_mapper[str(target_user.id)])
                topN_movies = []
                for idx in range(len(df)):
                    if df.iloc[idx].id not in target_user_watched:
                        topN_movies.append([df.iloc[idx].id, 0])
                for movie in topN_movies:
                    if str(movie[0]) in movie_mapper:
                        movie_id = int(movie_mapper[str(movie[0])])
                        movie[1] = np.dot(latent_movie[movie_id, :], np.transpose(latent_user[target_user_id, :]))
                topN_movies.sort(key=lambda movie: movie[1], reverse=True)
                topN_movies = topN_movies[:topN]

                movie_list = []
                for movie in topN_movies:
                    movie_list.append(movie[0])
                data = Movie.objects.filter(id__in=movie_list)
                print(data)

                serializer = RecommendMovie(data, many=True)
                return JsonResponse({'status': status.HTTP_200_OK, 'result': serializer.data}, safe=False)
        return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


@api_view(['GET', 'POST'])
def session_member(request):

    if request.method == 'GET': 
        try:
            token = request.GET.get('token', None)
            if not request.session.get(str(token)):
                request.session.save()
            user = User.objects.get(email=request.session.get(str(token)))
            
            if user is None:
                return JsonResponse({'msg': 'error', 'status': status.HTTP_400_BAD_REQUEST})

            if user.is_authenticated and token == str(Token.objects.get(user=user)):
                profile = Profile.objects.get(user=user)
                result = {
                    'email': user.email,
                    'username': profile.username,
                    'token': token,
                    'gender': profile.gender,
                    'age': profile.age,
                    'occupation': profile.occupation,
                    'is_auth': True,
                    'is_staff': profile.user.is_staff,
                    'movie_taste': profile.movie_taste
                }
            else:
                result = {
                    'email': None,
                    'username': None,
                    'token': None,
                    'gender': None,
                    'age': None,
                    'occupation': None,
                    'is_auth': False,
                    'is_staff': False,
                    'movie_taste': None
                }
            serializer = SessionSerializer(result)
            return JsonResponse({'result': serializer.data, 'status': status.HTTP_200_OK})
        except Exception:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})

    # if request.method == 'POST':

    #     result = {}
    #     token = request.data.get('token', None)
    #     email = request.session.get(str(token), None)
    #     user = User.objects.get(email=email)

    #     if user.is_authenticated and token == str(Token.objects.get(user=user)):
    #         profile = Profile.objects.get(user=user)
    #         print(profile)
    #         result = {
    #             'email': user.email,
    #             'username': profile.username,
    #             'token': token,
    #             'gender': profile.gender,
    #             'age': profile.age,
    #             'occupation': profile.occupation,
    #             'is_auth': True,
    #             'is_staff': profile.user.is_staff,
    #             'movie_taste': profile.movie_taste
    #         }
    #     else:
    #         result = {
    #             'email': None,
    #             'username': None,
    #             'token': None,
    #             'gender': None,
    #             'age': None,
    #             'occupation': None,
    #             'is_auth': False,
    #             'is_staff':  False,
    #             'movie_taste': profile.movie_taste
    #         }
    #     serializer = SessionSerializer(result)
    #     return JsonResponse({'result': serializer.data, 'status': status.HTTP_200_OK})
    # return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


@api_view(['GET'])
def duplicate_inspection(request):

    if request.method == 'GET':

        email = request.GET.get('email', None)

        if email is None:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'status': status.HTTP_200_OK})
        return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})
