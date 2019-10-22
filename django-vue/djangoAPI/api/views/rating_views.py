from rest_framework import status
from rest_framework.decorators import api_view
from api.serializers import RatingSerializer
from rest_framework.response import Response

from api.models import Rating, Movie, User, Comment

import datetime
import pytz

@api_view(['GET', 'POST'])
def ratings(request):

    if request.method == 'GET':
        
        serializer = RatingSerializer(ratings, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        params = request.data.get('params', None)
        userId = params.get('userId', None)
        movieId = params.get('movieId', None)
        rating = params.get('rating', None)
        timestamp = params.get('timestamp', None)
        content = params.get('content', None)
        
        print(userId, movieId, rating, timestamp, content)

        try:
            rating=Rating.objects.get(user__id=userId,movie__id=movieId)
        except Rating.DoesNotExist: #DoesNotExist 에러가 발행하면
            print('유저가 아직 해당 영화에 별점을 매기지 않았습니다.')
            user = User.objects.get(id = userId)
            movie = Movie.objects.get(id=movieId)
            rating=Rating(user=user,movie=movie,rating=rating,timestamp=timestamp)
            rating.save()
        
        if content:
            Comment(rating=rating,content=content).save()
            
        return Response(status=status.HTTP_201_CREATED)
