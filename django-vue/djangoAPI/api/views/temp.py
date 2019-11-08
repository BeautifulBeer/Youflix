from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import F
from django.http import JsonResponse
from api.models import Movie, User, Genre, Rating, Crew, Cast, UserCluster,Profile
from api.serializers import MovieSerializer, CrewSerializer, CastSerializer

@api_view(['GET'])
def temp(request):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        for pro in profiles:
            print(pro.id)
            if pro.id == 0:
                continue
            usercluster = UserCluster.objects.get(user_id=pro.id)
            clsuter = usercluster.kmeans_cluster
            pro.kmeans_cluster = clsuter
            pro.save()
        return JsonResponse({'status': status.HTTP_200_OK})
