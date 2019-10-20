from rest_framework import status
from rest_framework.decorators import api_view
# from django.contrib.auth.models import User
from api.serializers import RatingSerializer
from rest_framework.response import Response
from django.http import JsonResponse

from api.models import Rating
from api.models import Movie
from api.models import Profile
from api.models import Rating
from api.models import User

import datetime
import pytz


@api_view(['GET', 'POST'])
def ratings(request):

    if request.method == 'GET':
        
        serializer = RatingSerializer(ratings, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        ratings = request.data.get('ratings', None)

        for rating_obj in ratings:

            userId = rating_obj.get('userId', None)
            movieId = rating_obj.get('movieId', None)

            user = User.objects.get(username = 'user' + userId)
            movie = Movie.objects.get(id=movieId)

            rating = rating_obj.get('rating', None)
            timestamp = datetime.datetime.fromtimestamp(int(rating_obj.get('timestamp', None).strip())).replace(tzinfo=pytz.utc)

            if not (user and movie and rating and timestamp):
                continue
            if Rating.objects.filter(user = user).filter(movie = movie).count() > 0:
                continue

            age  = Profile.objects.get(user = user).age
            gender = Profile.objects.get(user = user).gender
            Rating(user=user, movie=movie, rating=rating, timestamp=timestamp).save()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def rate_movie(request):

    if request.method == 'GET':

        email = request.GET.get('email', None)
        movie_id = request.GET.get('movieId', None)
        rating_value = request.GET.get('ratingValue', None)

        if email is None or movie_id is None or rating_value is None:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})
       
        user = User.objects.get(email=email)
        movie = Movie.objects.get(id=movie_id)
        timestamp = datetime.datetime.fromtimestamp(int(rating_obj.get('timestamp', None).strip())).replace(tzinfo=pytz.utc)

        Rating(user=user, movie=movie, rating=rating_value, timestamp=timestamp).save()
        return JsonResponse({'status': status.HTTP_200_OK})
        