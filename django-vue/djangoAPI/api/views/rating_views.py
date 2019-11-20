from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from api.serializers import RatingSerializer, UserRatingSerializer
from api.models import Rating, Movie, Rating, User, Comment, Profile
import datetime
import pytz


@api_view(['GET'])
def rate_movie(request):

    if request.method == 'GET':

        email = request.GET.get('email', None)
        movie_id = request.GET.get('movie_id', None)
        rating_value = request.GET.get('ratingValue', None)

        if email is None or movie_id is None or rating_value is None:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})

        user = User.objects.get(email=email)
        movie = Movie.objects.get(id=movie_id)
        timestamp = datetime.datetime.now().replace(tzinfo=pytz.utc)

        try:
            existing_rating = Rating.objects.get(user=user, movie=movie)

            existing_rating.rating = rating_value
            existing_rating.timestamp = timestamp
            existing_rating.save()

        except Rating.DoesNotExist:
            Rating(user=user, movie=movie, rating=rating_value, timestamp=timestamp).save()
        return JsonResponse({'status': status.HTTP_200_OK})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


@api_view(['GET'])
def get_evaluate_rating(request):

    if request.method == 'GET':

        email = request.GET.get('email', None)
        movie_id = request.GET.get('movie_id', None)

        if email is None or movie_id is None:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})

        user = User.objects.get(email=email)
        movie = Movie.objects.get(id=movie_id)

        try:
            rating = Rating.objects.get(user=user, movie=movie)
        except Rating.DoesNotExist:
            return JsonResponse({'status': status.HTTP_200_OK, 'result': 0})
        return JsonResponse({'status': status.HTTP_200_OK, 'result': rating.rating})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


@api_view(['GET'])
def get_ratings(request):

    if request.method == 'GET':

        email = request.GET.get('email', None)

        if email is None:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})

        user = User.objects.get(email=email)
        ratings = Rating.objects.filter(user=user)
        serializer = UserRatingSerializer(ratings, many=True)
        return JsonResponse({'status': status.HTTP_200_OK, 'result': serializer.data})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})


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
            rating = Rating.objects.get(user__email=email, movie__id=movie_id)
            Comment(rating=rating, content=content, timestamp=timestamp).save()

        except Rating.DoesNotExist:
            # DoesNotExist 에러가 발행하면
            return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': '아직 해당 영화에 별점을 매기지 않았습니다.'})

        return JsonResponse({'status': status.HTTP_200_OK})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})
