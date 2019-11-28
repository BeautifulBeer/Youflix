from django.conf.urls import url
from api.views import movie_views
from api.views import auth_views
from api.views import rating_views
from api.views import recommend_views
from api.views import collabo_test
from api.views import content_based
from api.algorithms import kmeansClustering

urlpatterns = [
    # user 접근 URL
    url(r'auth/signup-many/$', auth_views.signup_many, name='sign_up_many'),
    url(r'auth/getUsers/$', auth_views.getUsers, name='get_users'),
    url(r'auth/deleteUser/$', auth_views.deleteUser, name='delete_user'),
    url(r'auth/similarUser/$', auth_views.similarUser, name='similarUser'),
    url(r'^auth/loginmember/$', auth_views.login, name='login_member'),
    url(r'^auth/registermember/$', auth_views.register, name='register_member'),
    url(r'^auth/logoutmember/$', auth_views.logout, name='logout_member'),
    url(r'^auth/session/$', auth_views.session_member, name="session_member"),
    url(r'^auth/updateUser/$', auth_views.updateUser, name="update_user"),
    url(r'^auth/predictRating/$', auth_views.predictMovieRating, name="predictRating"),

    # 중복체크 검사
    url(r'^auth/duplicateInspection/$', auth_views.duplicate_inspection, name="duplicate_inspection"),

    # movie 접근 URL
    url(r'movies/$', movie_views.movies, name='movie_list'),
    url(r'movies/pref/$', movie_views.moviesPref, name='movie_pref'),
    url(r'movies/views/$', movie_views.views, name='movie_views'),
    url(r'movies/modify/$', movie_views.modify, name='movie_modify'),
    url(r'movies/neverSeenMovies/$', movie_views.never_seen_movie_list, name='never_seen_movie_list'),
    url(r'movies/faculites/$', movie_views.faculites, name='faculites'),
    url(r'movies/rating/$', movie_views.get_rating_movie, name='get_rating_movie'),

    # 추천 URL
    url(r'^auth/recommendMovie/$', recommend_views.RecommendMovie, name='recommendMovie'),

    # 평점정보 접근 URL
    url(r'rateMovie/$', rating_views.rate_movie, name='rate_movie'),
    url(r'getRatings/$', rating_views.get_ratings, name='get_ratings'),
    url(r'getEvaluatedRating/$', rating_views.get_evaluate_rating, name='get_evaluate_rating'),
    url(r'ratings/comment/$', rating_views.create_comment, name='create_comment'),

    # clustering 실행 URL
    url('clustering/kmeansClustering/C/', kmeansClustering.C_Cluster, name="c_Cluster"),

    # Content-Based Algorithm
    url(r'preprocessing/$', content_based.preprocessing_for_cb, name='preprocessing'),
    url(r'content_based/$', content_based.algorithm, name='content_based')
]
