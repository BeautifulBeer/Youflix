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

url = os.path.join(BASE_DIR, 'data')
latent_user = np.load(os.path.join(url, 'mapper/latent_user.npy'))
latent_movie = np.load(os.path.join(url, 'mapper/latent_movie.npy'))
user_mapper = open(os.path.join(url, 'mapper/userMapper.json')).read()
user_mapper = json.loads(user_mapper)
movie_mapper = open(os.path.join(url, 'mapper/movieMapper.json')).read()
movie_mapper = json.loads(movie_mapper)

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
                    gender=gender,
                    movie_taste=None
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
            request.session.modified = True
            profile = Profile.objects.get(user=user)
            result = {
                'email': email,
                'id': profile.id,
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
                'id': None,
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
            request.session.modified = True
            result = {
                    'email': email,
                    'id': profile.id,
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


@api_view(['GET', 'POST'])
def session_member(request):

    if request.method == 'GET':
        try:
            token = request.GET.get('token', None)
            if not token:
                raise ValueError('No Token Parameter')
            # Request Session이 존재하지 않을 시에, logout 하고 재 로그인을 요청
            user = None
            if not request.session.get(str(token)):
                auth_user = Token.objects.get(key=token)
                user = User.objects.get(email=auth_user.user)
                if user is None:
                    raise User.DoesNotExist
                user.auth_token.delete()
                auth.logout(request)
                raise ValueError('Request session token key None')
            else:
                user = User.objects.get(email=request.session.get(str(token)))
                if user is None:
                    raise User.DoesNotExist
            if user.is_authenticated and token == str(Token.objects.get(user=user)):
                profile = Profile.objects.get(user=user)
                print('profile ID: ',profile.id)
                result = {
                    'email': user.email,
                    'id': profile.id,
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
                    'id': None,
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
            return JsonResponse({
                'result': serializer.data,
                'status': status.HTTP_200_OK
            })
        except ValueError:
            return JsonResponse({
                'status': status.HTTP_400_BAD_REQUEST,
                'msg': str(ValueError)
            })
        except User.DoesNotExist:
            return JsonResponse({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'msg': 'User does not Exists'
            })
        except Exception:
            return JsonResponse({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'msg': 'UNKNOWN ERROR'
            })

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

@api_view(['GET'])
def predictMovieRating(request):
    '''
        영화 m에 대한 유저 u의 예측평점을 반환하는 메서드입니다.
    '''
    try:
        if request.method == 'GET':
            movie_id = request.GET.get('movieId', None)
            useremail = request.GET.get('useremail', None)
            print('predictMovieRating ', movie_id, useremail)
            if movie_id is None or useremail is None:
                raise ValueError('Parameters are missing')
            user = User.objects.get(email=useremail)
            if user is None:
                raise User.DoesNotExist
            movie = Movie.objects.get(id=movie_id)
            if movie is None:
                raise Movie.DoesNotExist
            if str(user.id) not in user_mapper:
                raise KeyError('user id is invalid, mapper error')
            user_target_id = int(user_mapper[str(user.id)])
            if user_target_id is None:
                raise ValueError('user target id is none')
            if str(movie.id) not in movie_mapper:
                raise KeyError('movie id is invalid, mapper error')
            movie_target_id = int(movie_mapper[str(movie.id)])
            if movie_target_id is None:
                raise ValueError('movie target id is none')
            prediction = np.dot(
                latent_movie[movie_target_id, :],
                np.transpose(latent_user[user_target_id, :])
            )
            return JsonResponse({
                'status': status.HTTP_200_OK,
                'result': {
                    'prediction': prediction
                }
            })
    except ValueError as v:
        return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': str(v)})
    except User.DoesNotExist:
        return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'User Object is not exist'})
    except Movie.DoesNotExist:
        return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Movie Object is not exist'})
    except KeyError as k:
        return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': str(k)})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})
