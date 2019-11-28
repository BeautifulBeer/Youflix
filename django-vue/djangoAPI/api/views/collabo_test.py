from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from api.models import User, Movie

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



def collaborative_filtering(user, movies):
    # 1. 해당 유저의 예측 평점
    # user vector
    user_map = user_mapper[str(user.id)]
    user_vec = latent_user[user_map]

    predict_ratings = {}
    # movie vector
    for movieid in movies:
        try:
            movieId = None
            movieId = int(link[link['tmdbId'] == movieid]['movieId'])
            movie_map = movie_mapper[str(movieId)]
            movie_vec = latent_movie[movie_map]
            # 예측 평점
            predict = np.dot(user_vec, movie_vec.T)
            predict_ratings[movieid] = predict
        except KeyError:
            continue

    # 2. 예측 평점 topN movie
    movie_list = []
    rating_desc = sorted(predict_ratings.items(), key=lambda t: t[1], reverse=True)

    topN = 20
    if len(rating_desc) > topN:
        rating_desc = rating_desc[:topN]
    movie_list = [movie[0] for movie in rating_desc]
    return movie_list


def test(request):
    user = User.objects.get(id=2)
    movies = [16520, 1893, 85, 9087]
    collaborative_filtering(user, movies)
    return JsonResponse({'status': status.HTTP_200_OK}, safe=False)
