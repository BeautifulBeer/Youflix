from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from api.serializers import RatingSerializer
from rest_framework.response import Response

from api.models import Rating
from api.models import Movie
from api.models import Profile
from api.models import Rating

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
