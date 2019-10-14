from django.conf.urls import url
from api.views import movie_views
from api.views import auth_views
from api.views import rating_views
# from api.views import clustering
from api.views import test

urlpatterns = [
    # user 접근 URL
    url('auth/signup-many/$', auth_views.signup_many, name='sign_up_many'),
    url('auth/getUsers/$', auth_views.getUsers, name='get_users'),
    url('auth/deleteUser/$', auth_views.deleteUser, name='delete_user'),
    url('auth/similarUser/$', auth_views.similarUser, name='similarUser'),
    url('auth/recommendMovie/$', auth_views.RecommendMovieUserBased, name='recommendMovie'),
    url(r'^auth/loginmember/$', auth_views.login, name='login_member'),
    url(r'^auth/registermember/$', auth_views.register, name='register_member'),
    url(r'^auth/logoutmember/$', auth_views.logout, name='logout_member'),
    url(r'^auth/session/$', auth_views.session_member, name="session_member"),

    # movie 접근 URL
    url('movies/$', movie_views.movies, name='movie_list'),
    url('movies/pref/$', movie_views.moviesPref, name='movie_pref'),
    url('movies/views/$', movie_views.views, name='movie_views'),
    url('movies/modify/$', movie_views.modify, name='movie_modify'),
    
    url('similarMovie/$', movie_views.similarMovie, name='similarMovie'),
    url(r'^movies/recommend/$', movie_views.recommendation, name='movie_recommend'),

    # 평점정보 접근 URL
    url('ratings/$', rating_views.ratings, name='rating_list'),

    # clustering 실행 URL
    # url('clustering/userCharacter', clustering.getUserCharacter, name="getusercharacter"),
    # url('clustering/movieCharacter', clustering.getMovieCharacter, name="getmoviecharacter"),

    # TEST
    url('test/content', test.algo, name="alogTest")
]
