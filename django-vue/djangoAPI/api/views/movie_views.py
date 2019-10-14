from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import F
from api.models import Movie,User,Genre,Rating
from api.serializers import MovieSerializer,MovieAgeSerializer
from rest_framework.response import Response
from .tmdb import getMovieInfo
from django.core import serializers

import json
import operator

import requests
from bs4 import BeautifulSoup as bs
import openpyxl
from urllib.request import urlretrieve
import ssl

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def movies(request):

    if request.method == 'GET':
        id = request.GET.get('id', request.GET.get('movie_id', None))
        title = request.GET.get('title', None)
        genres = request.GET.get('genres', None)
        sort=request.GET.get('sort',1)
        page=request.GET.get('page',1)
        print(id, title, genres, sort, page)
        movies = Movie.objects.all()
        
        # querySet 으로 반환됨
        if id:
            movies = movies.filter(pk=id)
        if title:
            movies = movies.filter(title__icontains=title)
        if genres:
            if genres != 'Total':
                genre=Genre.objects.get(name=genres)
                movies = movies.filter(genres=genre)
        
        

        # 정렬방식
        if sort:
            if int(sort)==1: # 평균평점 순(높은순) default
                movies=movies.order_by(F('vote_average').desc(nulls_first=False))
            elif int(sort)==2: # 조회순
                movies=movies.order_by(F('view_cnt').desc(nulls_first=False))
            elif int(sort)==3: # 최신순
                movies=movies.order_by(F('release_date').desc(nulls_first=False))
            
            # 페이지 별로 나눠서 영화 정보 받아오기
            if page:
                # 한페이지에 10개씩. 1페이지 0~9, 2페이지 10~19, ... start= 10*(page-1), end=start+10
                # 10페이지 100 1 0~99 2 100~199
                # 영화 총개수: 3883. page=39이면 3800:3900 인덱스 에러. 
                page=int(page)
                start=50*(page-1)
                end=start+50
                if len(movies[start:])<50:
                    movies=movies[start:]
                movies=movies[start:end]
                
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        movie = Movie.objects.all()
        movie.delete()
        return Response(status=status.HTTP_200_OK)

    if request.method == 'POST':
        movies = request.data.get('movies', None)
        for movie in movies:
            id = movie.get('id', None)
            id=int(id)
            title = movie.get('title', None)
            genres = movie.get('genres', None)

            try:
                if title[-1]=='"':
                    only_title=title[1:len(title)-7]
                    year=int(title[len(title)-6:len(title)-2])
                elif title[-1]==" ":
                    only_title=title[:len(title)-8]
                    year=int(title[len(title)-6:len(title)-2])
                else:
                    only_title=title[:len(title)-6]
                    year=int(title[len(title)-5:len(title)-1])
            except ValueError:
                only_title=title
                year=0
            
            if not (id and title and genres):
                continue
            # if Movie.objects.filter(id=id).count() > 0 or Movie.objects.filter(title=title).count() > 0:
            #     continue
            
            Movie(id=id, title=only_title, year=year, genres='|'.join(genres)).save()

        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def views(request):

    if request.method == 'GET':

        id = request.GET.get('id', None)

        if id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        movie = Movie.objects.get(pk=id)
        movie.view_cnt = movie.view_cnt + 1
        movie.save()

        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def similarMovie(request):
        
    if request.method == 'GET':
        id=request.GET.get('id', None)
        
        if id:
            movie=Movie.objects.get(movie__id=id)
            movie_cluster=movie.kmeans_cluster
            movies=Movie.objects.filter(cluster=movie_cluster)

        serializer = SimilarMovieSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def modify(request):

    if request.method == 'POST':

        modified = request.data.get('data', None)        
        print(modified)
        
        id = modified.get('id', None)
        title = modified.get('title', None)
        overview = modified.get('overview', None)
        genres = modified.get('genres_array', None)
        runtime = modified.get('runtime', None)

        if id is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        movie = Movie.objects.get(pk=id)
        
        movie.title = title
        movie.overview = overview
        movie.genres = ','.join(genres)
        movie.runtime = runtime

        movie.save()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def moviesPref(request):

    if request.method == 'GET':
        
        email = request.GET.get('email', None)

        print(email)


        if email is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email)
        print(user)
        ratings = Rating.objects.filter(user=user)

        ret = dict([("0.5", 0), ("1", 0), ("1.5", 0), ("2", 0), ("2.5", 0), ("3", 0), ("3.5", 0), ("4", 0), ("4.5", 0), ("5", 0)])
        print(ratings)
        print(ret)
        for rating in ratings:

            print(rating.rating)

            if rating.rating < 1:
                ret['0.5'] = ret.get('0.5') + 1
            elif rating.rating < 1.5:
                ret['1'] = ret.get('1') + 1
            elif rating.rating < 2:
                ret['1.5'] = ret.get('1.5') + 1
            elif rating.rating < 2.5:
                ret['2'] = ret.get('2') + 1
            elif rating.rating < 3:
                ret['2.5'] = ret.get('2.5') + 1
            elif rating.rating < 3.5:
                ret['3'] = ret.get('3') + 1
            elif rating.rating < 4:
                ret['3.5'] = ret.get('3.5') + 1
            elif rating.rating < 4.5:
                ret['4'] = ret.get('4') + 1
            elif rating.rating < 5:
                ret['4.5'] = ret.get('4.5') + 1
            else:
                ret['5'] = ret.get('5') + 1

        # json_ret = json.dumps(ret)
        print(ret)
        return Response(data=ret, status=status.HTTP_200_OK)

@api_view(['GET'])
def recommendation(request):
    print(request.GET.get('id'), None)
    if request.method == 'GET':
        topN_movies = [469172, 267752, 404604,
            459950, 458506, 456101, 455675,	454787,
            452413, 452068, 408509, 1271]

        movies = Movie.objects.all()

        result = movies.filter(id__in=topN_movies)
        serializer = MovieSerializer(result, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
