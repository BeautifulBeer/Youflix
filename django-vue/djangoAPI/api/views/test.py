from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Movie, Rating, User, Crew
# from django.contrib.auth.models import User
from api.serializers import MovieSerializer,MovieAgeSerializer,MovieGenderSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from .tmdb import getMovieInfo

import json
import operator

import re
import os
import math
import time

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

# Numba
from numba import jit
import numba

from scipy import sparse
import sklearn.preprocessing as pp

@api_view(['GET'])
def content_based(request):

    if request.method == 'GET':

        email = request.GET.get('email', None)
        user = User.objects.get(email=email)
        ratings = Rating.objects.filter(user=user)

        movie_obj = []
        selected_movies = []
        selected_movies_index = []

        for rating in ratings:
            movie_obj.append(rating.movie)

        # Read preprocessing data
        def_keywords = pd.read_csv('def_keywords.csv')
        preprocessing_data = pd.read_csv('preprocessing.csv')

        for movie in movie_obj:
            selected_movies.append(def_keywords.loc[def_keywords['id'] == movie.id])
            selected_movies_index.append(def_keywords.loc[def_keywords['id'] == movie.id].index.values[0])
        print(selected_movies_index)

        preprocessing_data['overview'] = preprocessing_data['overview'].fillna('')

        tfidf = TfidfVectorizer(stop_words='english')

        # <class 'numpy.ndarray'>
        tfidf_matrix_overview = tfidf.fit_transform(preprocessing_data['overview'])
        print(tfidf_matrix_overview)
        # overview_total = get_total_tf_idf(tfidf_matrix_overview.toarray())
        
        # tfidf_matrix_overview = tfidf_matrix_overview.toarray()
        overview_matrix = np.array(get_extracted_list(tfidf_matrix_overview.toarray(), selected_movies_index))
        # ret = np.zeros((len(overview_matrix), len(overview_matrix[0])), dtype=np.float64)

        print("CALCULATE> ")
        print("OVERVIEW MATRIX>")
        print(overview_matrix)
        print()
        print("TFIDF TOTAL MATRIX>")
        print(tfidf_matrix_overview)
        print()
        print(type(overview_matrix), " ", type(tfidf_matrix_overview))
        # print(len(overview_matrix), " ", len(tfidf_matrix_overview))
        print(tfidf_matrix_overview.getnnz())

        overview_matrix = adjust_similarity_values(overview_matrix, np.zeros((len(overview_matrix), len(overview_matrix[0])), dtype=np.float64))
        print(type(overview_matrix))
        print()

        print("BEFORE")
        print(tfidf_matrix_overview)
        print()

        for row in range(45432):
            for index in range(len(tfidf_matrix_overview[row].indices)):
                tfidf_matrix_overview[row].data[index] /= 205631.73694292648
        print("AFTER")
        print(tfidf_matrix_overview)
        # tfidf_matrix_overview = adjust_similarity_values(tfidf_matrix_overview, np.zeros((len(tfidf_matrix_overview), len(tfidf_matrix_overview[0])), dtype=np.float64))
        

        tfidf_sparse_matrix_overview = sparse.csr_matrix(tfidf_matrix_overview)
        sparse_partial_matrix_overview = sparse.csr_matrix(overview_matrix)
        # print("SPARSE COMPLETE")
        # print(cosine_similarity(tfidf_sparse_matrix_overview, dense_output=False))
        overview_similarity = linear_kernel(sparse_partial_matrix_overview, tfidf_sparse_matrix_overview, dense_output=False)
        # print()

        tfidf_matrix_title = tfidf.fit_transform(preprocessing_data['title'])
        tfidf_matrix_title = tfidf_matrix_title.toarray()
        title_matrix = np.array(get_extracted_list(tfidf_matrix_title, selected_movies_index))
        # title_matrix = title_matrix.toarray()
        title_matrix = adjust_similarity_values(title_matrix, 'TITLE_TF_IDF_TOTAL_VALUE')
        print("TITLE MATRIX> ")
        title_similarity = linear_kernel(title_matrix, tfidf_matrix_title)
        print(title_similarity)


        # scikit-learn의 CountVectorizer를 사용하여 키워드를 토큰화하여 행렬을 조사하여 각 단어의 빈도를 분석합니다.
        cv = CountVectorizer()
        cv_mx = cv.fit_transform(def_keywords['keywords'])

        result = np.ndarray(shape = (1, 45433), dtype = float)

        index = 0
        offset = 0

        for selected in selected_movies:

            idx = selected.index.values[0]
            # Cosine Similarity 알고리즘을 사용하여 유사도를 분석합니다.
            cosine_sim = cosine_similarity(cv_mx[idx:idx + 1], cv_mx)

            # 유저가 점수를 매긴 값을 지수승으로 곱해줍니다.
            offset = math.exp(ratings[index].rating)

            for i in range(len(cosine_sim[0])):
                result[0][i] += cosine_sim[0][i] * int(offset)
            index += 1

        # 일치하는 index list를 생성합니다.
        indices = pd.Series(df_keys.index, index = df_keys['id'])

        # 상위 10개의 추천 영화를 추출합니다.
        serializer = MovieSerializer(get_movie_list(df_keys, recommend_movie(df_keys, indices, 597, result, 50)), many=True)
        print(serializer)
        return JsonResponse({'status': status.HTTP_200_OK, 'result': serializer.data}, safe=False)


def cosine_similarities(mat):
    col_normed_mat = pp.normalize(mat.tocsc(), axis=0)
    return col_normed_mat.T * col_normed_mat
# @numba.jit(target='cpu', nopython=True, parallel=True)
# def fast_cosine_matrix(u, M):
#     scores = np.zeros(M.shape[0])
#     for i in numba.prange(M.shape[0]):
#         v = M[i]
#         m = u.shape[0]
#         udotv = 0
#         u_norm = 0
#         v_norm = 0
#         for j in range(m):
#             if (np.isnan(u[j])) or (np.isnan(v[j])):
#                 continue

#             udotv += u[j] * v[j]
#             u_norm += u[j] * u[j]
#             v_norm += v[j] * v[j]

#         u_norm = np.sqrt(u_norm)
#         v_norm = np.sqrt(v_norm)

#         if (u_norm == 0) or (v_norm == 0):
#             ratio = 1.0
#         else:
#             ratio = udotv / (u_norm * v_norm)
#         scores[i] = ratio
#     return scores

@jit(nopython=True)
def get_total_tf_idf(matrix):

    ret = 0.0
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            ret += matrix[row][col]
    return ret


@jit(nopython=True)
def adjust_similarity_values(similarity_matrix, ret):

    for row in range(len(similarity_matrix)):
        for col in range(len(similarity_matrix[row])):
            if similarity_matrix[row][col] != 0:
                ret[row][col] = (similarity_matrix[row][col] / 205631.73694292648)
    return ret


def get_extracted_list(matrix, index_list):

    ret = []
    for index in index_list:
        ret.append(matrix[index, :])
    return ret

def get_movie_list(df_keys, datas):

    movie_list = []
    for index in datas.index:
        movie_list.append(Movie.objects.get(pk=df_keys.iloc[index]['id']))
    return movie_list

@api_view(['GET'])
def algo(request):
    
    print("TEST")
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
    movies_frame = movies_frame.drop('original_title', axis=1)
    movies_frame = movies_frame.drop('original_language', axis=1)

    # 각 영화에 대한 Keyword와 Genre를 추출합니다.
    keywords = []
    genres = []

    # DataFrame을 하나씩 참조하며 해당 영화에 맞는 Keyword와 Genre들을 저장합니다.
    # 없을 경우 ''을 삽입 합니다.
    for element in movies_frame.values:

        # id를 통해 movie 객체를 가져와서 필요한 정보를 추출합니다.
        movie = Movie.objects.get(id=element[0])

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
    pd.set_option('display.max_columns', 30)

    # 데이터 전처리 및 생성
    # 1. overview가 없는 영화에 대해서 ''로 모두 할당 해줍니다.
    movies_frame['overview'] = movies_frame['overview'].fillna('')
    # 2. Genre 데이터를 삽입합니다.
    movies_frame = movies_frame.assign(genres=genres)
    # 3. Keyword 데이터를 삽입합니다.
    movies_frame = movies_frame.assign(keywords=keywords)

    print(movies_frame.head())

    # genres, keywords 데이터에 대해서 공백(' ')을 없애줍니다.
    movies_frame['genres'] = movies_frame['genres'].apply(preprocessing_genres)
    movies_frame['keywords'] = movies_frame['keywords'].apply(preprocessing_keyword)

    movies_frame.to_csv('preprocessing.csv', mode='w')

    # Rake(Rapid Automatic Keyword Extraction)을 이용해서 줄거리에 대한 keyword을 추출합니다.
    # movies_frame['overview'] = movies_frame['overview'].apply(preprocessing_overview)

    # TF-IDF(Term Frequency - Inverse Document Frequency)을 이용해서 Overview와 Title의 Keyword를 추출합니다.
    # tfidf = TfidfVectorizer(stop_words='english')
    # tfidf_matrix = tfidf.fit_transform(movies_frame['title'])

    # cosine_sim = get_similarity(linear_kernel(tfidf_matrix, tfidf_matrix))

    # tfidf = TfidfVectorizer(stop_words='english')
    # tfidf_matrix = tfidf.fit_transform(movies_frame['overview'])

    # cosine_sim = get_similarity(linear_kernel(tfidf_matrix, tfidf_matrix))

    # 앞에서 만든 데이터를 통하여 새로운 DataFrame을 생성합니다.
    df_keys = pd.DataFrame()
    # df_keys['title'] = movies_frame['title']
    df_keys['keywords'] = ''
    df_keys['id'] = movies_frame['id']

    # 만들어진 단어들을 하나의 단어 모음으로 만듭니다.
    df_keys['keywords'] = movies_frame.apply(bag_words, axis=1)

    # 지금까지의 결과를 .csv 파일로 저장합니다.
    df_keys.to_csv('def_keywords.csv', mode='w')

    # test 출력
    # print(df_keys.head())

    # scikit-learn의 CountVectorizer를 사용하여 키워드를 토큰화하여 행렬을 조사하여 각 단어의 빈도를 분석합니다.
    # cv = CountVectorizer()
    # cv_mx = cv.fit_transform(df_keys['keywords'])

    # Cosine Similarity 알고리즘을 사용하여 유사도를 분석합니다.
    # cosine_sim = cosine_similarity(cv_mx, cv_mx)
    # pd.DataFrame(cosine_sim).to_csv('consine_sim.csv', mode='w')
    # test 출력
    # print(cosine_sim)

    # 일치하는 index list를 생성합니다.
    # indices = pd.Series(df_keys.index, index=df_keys['id'])

    # 상위 10개의 추천 영화를 추출합니다.
    # print(recommend_movie(df_keys, indices, 597, cosine_sim, 10))
    return Response(status=status.HTTP_200_OK)

@jit(nopython=True)
def get_similarity(cosine_sim):

    row_total = 0.0

    print("BEFORE")
    print(cosine_sim)
    print()

    for row in range(len(cosine_sim)):

        for col in range(len(cosine_sim[row])):
            row_total += cosine_sim[row][col]
        
        for col in range(len(cosine_sim[row])):
            if cosine_sim[row][col] == 0:
                continue
            cosine_sim[row][col] / row_total
        row_total = 0.0

    print()
    print("AFTER")
    print(cosine_sim)

    return cosine_sim


def recommend_movie(df_keys, indices, id, cosine_sim, n):

    movies = []

    # 일치하는 영화가 있는지 검사합니다.
    if id not in indices.index:
        print("Movie not in database.")
        return

    # 내림차순으로, Cosine Simirality을 정렬합니다.
    scores = pd.Series(cosine_sim[0]).sort_values(ascending = False)

    # 가장 유사한 n(10)개만 추출합니다.
    # 첫번째 index의 영화의 경우 활성화된 영화와 같기 때문에 제외합니다.
    top_n_idx = list(scores.iloc[1:n].index)

    # 타이틀을 기준으로 추출합니다.
    return df_keys['title'].iloc[top_n_idx]


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

    return (' '.join(x['genres']) + ' ' + ' '.join(x['keywords']))
