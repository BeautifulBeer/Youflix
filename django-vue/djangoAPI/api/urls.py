from django.conf.urls import url
from api.views import movie_views
from api.views import auth_views
from api.views import rating_views
# from api.views import clustering
from api.views import test

urlpatterns = [
    # user 접근 URL
    url(r'auth/signup-many/$', auth_views.signup_many, name='sign_up_many'),
    url(r'auth/getUsers/$', auth_views.getUsers, name='get_users'),
    url(r'auth/deleteUser/$', auth_views.deleteUser, name='delete_user'),
    url(r'auth/similarUser/$', auth_views.similarUser, name='similarUser'),
    url(r'auth/recommendMovie/$', auth_views.RecommendMovieUserBased, name='recommendMovie'),
    url(r'^auth/loginmember/$', auth_views.login, name='login_member'),
    url(r'^auth/registermember/$', auth_views.register, name='register_member'),
    url(r'^auth/logoutmember/$', auth_views.logout, name='logout_member'),
    url(r'^auth/session/$', auth_views.session_member, name="session_member"),
    url(r'^auth/updateUser/$', auth_views.updateUser, name="update_user"),

    # 중복체크 검사
    url(r'^auth/duplicateInspection/$', auth_views.duplicate_inspection, name="duplicate_inspection"),
    
    # movie 접근 URL
    url(r'movies/$', movie_views.movies, name='movie_list'),
    url(r'movies/pref/$', movie_views.moviesPref, name='movie_pref'),
    url(r'movies/views/$', movie_views.views, name='movie_views'),
    url(r'movies/modify/$', movie_views.modify, name='movie_modify'),
    url(r'similarMovie/$', movie_views.similarMovie, name='similarMovie'),
    url(r'^movies/recommend/$', movie_views.recommendation, name='movie_recommend'),

    # 평점정보 접근 URL
    url(r'ratings/$', rating_views.ratings, name='rating_list'),

    # clustering 실행 URL
    # url('clustering/userCharacter', clustering.getUserCharacter, name="getusercharacter"),
    # url('clustering/movieCharacter', clustering.getMovieCharacter, name="getmoviecharacter"),
]
