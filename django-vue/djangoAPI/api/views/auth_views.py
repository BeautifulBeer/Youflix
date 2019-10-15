from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.core.cache import cache

from api.serializers import ProfileSerializer,SessionSerializer,RecommendMovie,SimilarUserSerializer
# from api.serializers import SimilarUserSerializer

# from api.models import UserCluster
from api.models import create_profile
from api.models import User,Profile,Movie,Rating,UserCluster

from django.shortcuts import render
from django.contrib import auth

from rest_framework.authtoken.models import Token

from collections import Counter
import pandas as pd
from django_pandas.io import read_frame
import json
import numpy as np

import logging
logger = logging.getLogger("mylogger")

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@api_view(['POST'])
def signup_many(request):

    if request.method == 'POST':
        profiles = request.data.get('profiles', None)
        for profile in profiles:
            email = profile.get('email', None)
            username = profile.get('username', None)
            password = profile.get('password', None)
            age = profile.get('age', None)
            occupation = profile.get('occupation', None)
            gender = profile.get('gender', None)

            create_profile(email=email, username=username,password=password, age=age,
                           occupation=occupation, gender=gender)

        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getUsers(request):

    if request.method == 'GET':
        age=request.GET.get('age', None)
        gender=request.GET.get('gender', None)
        occupation=request.GET.get('occupation', None)
        page=request.GET.get('page', 1)
            
        profiles = Profile.objects.all()
        if age:
                profiles=profiles.filter(age=age)
        if gender:
                profiles=profiles.filter(gender=gender)
        if occupation:
                profiles=profiles.filter(occupation=occupation)
        if page:
            page=int(page)
            if page<=len(profiles)//50+1:
                start=50*(page-1)
                end=start+50
                if len(profiles[start:])<50:
                    profiles=profiles[start:]
                profiles=profiles[start:end]

        serializer = ProfileSerializer(profiles, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
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
                print(email, username, password, age, gender, occupation, genres)
        try:         
                create_profile(email=email, username=username, password=password, age=age, occupation=occupation, gender=gender, movie_taste=genres)
        except:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
        print('login request')
        if request.method == 'POST':
                email = request.data.get('email', None)
                password = request.data.get('password', None)

                if email is None or password is None:
                        return Response(data="Not input ID and Password", status=status.HTTP_400_BAD_REQUEST)
                if email is None:
                        return Response(data="Not input Email", status=status.HTTP_400_BAD_REQUEST)
                if password is None:
                        return Response(data="Not input Password", status=status.HTTP_400_BAD_REQUEST)

                user = auth.authenticate(email=email, password=password)
                if user :
                        auth.login(request, user)
                        token = Token.objects.create(user=user)
                        request.session[str(token)] = email
                        profile = Profile.objects.get(user=user)
                        result = {
                                'email': email,
                                'username' : profile.username,
                                'gender': profile.gender,
                                'age': profile.age,
                                'occupation': profile.occupation,
                                'token' : token,
                                'is_staff' : profile.user.is_staff,
                                'is_auth' : True,
                                'movie_taste': profile.movie_taste
                        }
                else : 
                        result = {
                                'email': None,
                                'username' : None,
                                'gender': None,
                                'age': None,
                                'occupation': None,
                                'token' : None,
                                'is_staff' : False,
                                'is_auth' : False,
                                'movie_taste': None
                        }
                serializer = SessionSerializer(result)
                return Response(data = serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def logout(request):
        print(request)
        if request.method == 'POST':
                token = request.data.get('token', None)
                user = User.objects.get(email=request.session[str(token)])
                del request.session[str(token)]
                user.auth_token.delete()
                auth.logout(request)
        return Response(status=status.HTTP_200_OK)
        

@api_view(['DELETE'])
def deleteUser(request):

        if request.method == 'DELETE':
                id = request.GET.get('id', None)
                users = User.objects.all()
                user = users.get(id=id)
                user.delete()

                return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def updateUser(request):

        if request.method == 'POST':

                params = request.data.get('params', None)

                email = params.get('email', None)
                username = params.get('username', None)
                password = params.get('password', None)
                occupation = params.get('occupation', None)
                genres = params.get('genres', None)

                print(email)
                print(username)
                print(password)
                print(occupation)
                print(genres)

                user = User.objects.get(email=email)
                profile = Profile.objects.get(user=user)

                print()
                print(user)
                print(profile)

                user.set_password(password)
                user.save()

                genres_ = ','.join(genres)

                profile.username = username
                profile.occupation = occupation
                profile.genres = genres_
                profile.save()

                return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def similarUser(request):
        
    if request.method == 'GET':
        target_id=request.GET.get('id', None)
        
        if target_id:
                target_user=Profile.objects.get(id=target_id)
                target_cluster=target_user.kmeans_cluster
                similar_users=Profile.objects.filter(kmeans_cluster=target_cluster)
                similar_users=similar_users.exclude(id=target_id)

        serializer = SimilarUserSerializer(similar_users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
import time
import copy

url=os.path.join(BASE_DIR, 'data', 'mapper')
latent_user = np.load(os.path.join(url, 'latent_user.npy'))
latent_movie = np.load(os.path.join(url, 'latent_movie.npy'))
user_mapper=open(os.path.join(url,'userMapper.json')).read()
user_mapper = json.loads(user_mapper)
movie_mapper=open(os.path.join(url,'movieMapper.json')).read()
movie_mapper = json.loads(movie_mapper)

@api_view(['GET'])
def RecommendMovieUserBased(request):
        start=time.time()
        topN = 20
        if request.method == 'GET':

                target_id=request.GET.get('id', None)
                if target_id:
                        # 1. target_id user와 같은 군집인 users
                        target_user=Profile.objects.get(id=target_id)
                        target_cluster=target_user.kmeans_cluster
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
                                similar_users=Profile.objects.filter(kmeans_cluster=target_cluster)
                                similar_user_list=[user.id for user in similar_users]

                                # 2. 해당 군집 모든 유저가 가장 많이 시청한 영화
                                movie_list=[]
                                for userid in similar_user_list:
                                        ratings=Rating.objects.filter(user__id=userid)
                                        for rating in ratings:
                                                movie_list.append(rating.movie.id) 

                                movie_counts = Counter(movie_list)
                                movie_dict=dict(movie_counts)
                                df=pd.DataFrame(list(movie_dict.items()),columns=['id','count'])
                                # 5개 미만의 평점수를 가진 영화 제거
                                df=df[df['count']>=5]
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
                        topN_movies.sort(key=lambda movie : movie[1], reverse=True)
                        topN_movies = topN_movies[:topN]
                        
                        movie_list=[]
                        for movie in topN_movies:
                                movie_list.append(movie[0])
                        data=Movie.objects.filter(id__in=movie_list)
                        print(data)
                        
                        serializer = RecommendMovie(data, many=True)
                        return Response(data=serializer.data, status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def session_member(request):

        if request.method == 'POST':

                result = {}
                token = request.data.get('token', None)
                email = request.session.get(str(token), None)
                user = User.objects.get(email=email)

                if user.is_authenticated and token == str(Token.objects.get(user=user)):
                        profile = Profile.objects.get(user=user)
                        print(profile)
                        result = {
                                'email' : user.email,
                                'username' : profile.username,
                                'token' : token,
                                'gender': profile.gender,
                                'age': profile.age,
                                'occupation': profile.occupation,
                                'is_auth' : True,
                                'is_staff' : profile.user.is_staff,
                                'movie_taste': profile.movie_taste
                        }
                else :
                        result = {
                                'email': None,
                                'username' : None,
                                'token' : None,
                                'gender': None,
                                'age': None,
                                'occupation': None,
                                'is_auth' : False,
                                'is_staff' :  False,
                                'movie_taste': profile.movie_taste
                        }
                serializer = SessionSerializer(result)
                return Response(data = serializer.data, status=status.HTTP_200_OK)

        if request.method == 'GET': 

                result = {
                        'msg' : 'error'
                }
                token = request.GET.get('token', None)
                email = request.session.get(str(token), None)
                user = None

                if email is not None:
                        user = User.objects.get(email=email)
                else:
                        return Response(data = result, status=status.HTTP_400_BAD_REQUEST)

                if user.is_authenticated and token == str(Token.objects.get(user=user)):
                        profile = Profile.objects.get(user=user)
                        result = {
                                'email' : user.email,
                                'username' : profile.username,
                                'token' : token,
                                'gender': profile.gender,
                                'age': profile.age,
                                'occupation': profile.occupation,
                                'is_auth' : True,
                                'is_staff' : profile.user.is_staff,
                                'movie_taste': profile.movie_taste
                        }
                else : 
                        result = {
                                'email' : None,
                                'username': None,
                                'token' : None,
                                'gender': None,
                                'age': None,
                                'occupation': None,
                                'is_auth' : False,
                                'is_staff' : False,
                                'movie_taste': None
                        }
                serializer = SessionSerializer(result)
                return Response(data = serializer.data, status=status.HTTP_200_OK)
