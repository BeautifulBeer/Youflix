from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import F
from django.http import JsonResponse
from api.models import Movie, User, Genre, Rating
from api.serializers import MovieSerializer


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def movies(request):
    '''
        영화를 CRUD할 수 있는 URL
    '''
    if request.method == 'GET':
        movie_id = request.GET.get('id', request.GET.get('movie_id', None))
        title = request.GET.get('title', None)
        category = request.GET.get('category', None)
        keyword = request.GET.get('keyword', None)
        sort = request.GET.get('sort', 1)
        page = request.GET.get('page', 1)
        print(movie_id, title, category, keyword, sort, page)
        movie_all = Movie.objects.all()

        # querySet 으로 반환됨
        if movie_id:
            movie_all = movie_all.filter(pk=movie_id)
        if title:
            movie_all = movie_all.filter(title__icontains=title)
        if category == 'genre':
            if keyword != 'Total':
                genre_obj = Genre.objects.get(name=keyword)
                movie_all = movie_all.filter(genres=genre_obj)

        # 정렬방식
        if sort:
            if int(sort) == 1:
                # 평균평점 순(높은순) default
                movie_all = movie_all.order_by(F('vote_average').desc(nulls_first=False))
            elif int(sort) == 2:
                # 조회순
                movie_all = movie_all.order_by(F('view_cnt').desc(nulls_first=False))
            elif int(sort) == 3:
                # 최신순
                movie_all = movie_all.order_by(F('release_date').desc(nulls_first=False))

            # 페이지 별로 나눠서 영화 정보 받아오기
            if page:
                # 한페이지에 10개씩. 1페이지 0~9, 2페이지 10~19, ... start= 10*(page-1), end=start+10
                # 10페이지 100 1 0~99 2 100~199
                # 영화 총개수: 3883. page=39이면 3800:3900 인덱스 에러.
                page = int(page)
                start = 50*(page-1)
                end = start+50
                if len(movie_all[start:]) < 50:
                    movie_all = movie_all[start:]
                movie_all = movie_all[start:end]

        serializer = MovieSerializer(movie_all, many=True)
        return JsonResponse({'status': status.HTTP_200_OK, 'result': serializer.data}, safe=False)

    if request.method == 'DELETE':
        movie = Movie.objects.all()
        movie.delete()
        return JsonResponse({'status': status.HTTP_200_OK})

    if request.method == 'POST':
        movie_all = request.data.get('movies', None)
        for movie in movie_all:
            movie_id = movie.get('id', None)
            movie_id = int(movie_id)
            title = movie.get('title', None)
            genres = movie.get('genres', None)

            try:
                if title[-1] == '"':
                    only_title = title[1:len(title)-7]
                    year = int(title[len(title)-6:len(title)-2])
                elif title[-1] == " ":
                    only_title = title[:len(title)-8]
                    year = int(title[len(title)-6:len(title)-2])
                else:
                    only_title = title[:len(title)-6]
                    year = int(title[len(title)-5:len(title)-1])
            except ValueError:
                only_title = title
                year = 0

            if not (movie_id and title and genres):
                continue
            # if Movie.objects.filter(id=id).count() > 0 or Movie.objects.filter(title=title).count() > 0:
            #     continue

            Movie(id=movie_id, title=only_title, year=year, genres='|'.join(genres)).save()

        return JsonResponse({'status': status.HTTP_200_OK})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})

@api_view(['GET'])
def views(request):
    if request.method == 'GET':

        movie_id = request.GET.get('id', None)

        if movie_id is None:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})

        movie = Movie.objects.get(pk=movie_id)
        movie.view_cnt = movie.view_cnt + 1
        movie.save()

        return JsonResponse({'status': status.HTTP_200_OK})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})

@api_view(['POST'])
def modify(request):

    if request.method == 'POST':

        modified = request.data.get('data', None)
        print(modified)

        movie_id = modified.get('id', None)
        title = modified.get('title', None)
        overview = modified.get('overview', None)
        genres = modified.get('genres_array', None)
        runtime = modified.get('runtime', None)

        if movie_id is None:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})

        movie = Movie.objects.get(pk=movie_id)

        movie.title = title
        movie.overview = overview
        movie.genres = ','.join(genres)
        movie.runtime = runtime

        movie.save()
        return JsonResponse({'status': status.HTTP_200_OK})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})

@api_view(['GET'])
def moviesPref(request):

    if request.method == 'GET':

        email = request.GET.get('email', None)
        print(email)

        if email is None:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})

        user = User.objects.get(email=email)
        ratings = Rating.objects.filter(user=user)

        ret = dict([
            ("0.5", 0),
            ("1", 0),
            ("1.5", 0),
            ("2", 0),
            ("2.5", 0),
            ("3", 0),
            ("3.5", 0),
            ("4", 0),
            ("4.5", 0),
            ("5", 0)
        ])
        for rating in ratings:

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

            print(ret)
        return JsonResponse({'status': status.HTTP_200_OK, 'data': ret})
    return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Invalid Request Method'})