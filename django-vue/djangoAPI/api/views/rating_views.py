from rest_framework import status
from rest_framework.decorators import api_view
from api.serializers import RatingSerializer
from rest_framework.response import Response
from django.http import JsonResponse

from api.models import Rating, Movie, User, Comment

import datetime
import pytz

@api_view(['GET'])
def create_comment(request):

    if request.method == 'GET':

        email = request.GET.get('email', None)
        movie_id = request.GET.get('movie_id', None)
        content = request.GET.get('content', None)

        if email is None or movie_id is None or content is None:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})
       
        timestamp = datetime.datetime.now().replace(tzinfo=pytz.utc)

        try:
            rating=Rating.objects.get(user__email=email,movie__id=movie_id)
            Comment(rating=rating,content=content,timestamp=timestamp).save()

        except Rating.DoesNotExist: #DoesNotExist 에러가 발행하면
            print('유저가 아직 해당 영화에 별점을 매기지 않았습니다.')
            return

        return JsonResponse({'status': status.HTTP_200_OK})
