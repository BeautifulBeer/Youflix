from .models import Profile, Movie, Rating, UserCluster
from .models import User, Crew
from rest_framework import serializers

import json

# ================= User Serializer =================== #


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    email = serializers.SerializerMethodField('get_email')
    is_staff = serializers.SerializerMethodField('get_is_staff')
    movie_tastes = serializers.SerializerMethodField('get_movie_taste')

    class Meta:
        model = Profile
        fields = ('id', 'user', 'email', 'username', 'is_staff', 'gender', 'age', 'occupation', 'movie_taste')

    def get_email(self, obj):
        return obj.user.email

    def get_is_staff(self, obj):
        return obj.user.is_staff

    def get_movie_taste(self, obj):
        return obj.movie_taste


class SimilarUserSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField('get_profile')

    class Meta:
        model = UserCluster
        fields = ('profile', 'kmeans_cluster', 'user_info')

    def get_profile(self, obj):
        profile = {'email': obj.profile.user.email, 'age': obj.profile.age, 'gender': obj.profile.gender, 'occupation': obj.profile.occupation}
        return profile


class RecommendMovie(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField('getGenre')
    production_companies = serializers.SerializerMethodField('getCompany')
    production_countries = serializers.SerializerMethodField('getCountry')
    spoken_languages = serializers.SerializerMethodField('getLanguage')
    keywords = serializers.SerializerMethodField('getKeyword')

    class Meta:
        model = Movie
        fields = '__all__'

    def getGenre(self, obj):
        genres = obj.genres.all()
        genre_list = []
        for genre in genres:
            genre_list.append(genre.name)
        return genre_list

    def getCompany(self, obj):
        companies = obj.production_companies.all()
        company_list = []
        for company in companies:
            company_list.append(company.name)
        return company_list

    def getCountry(self, obj):
        countries = obj.production_countries.all()
        country_list = []
        for country in countries:
            country_list.append(country.name)
        return country_list

    def getLanguage(self, obj):
        languages = obj.spoken_languages.all()
        language_list = []
        for language in languages:
            language_list.append(language.name)
        return language_list

    def getKeyword(self, obj):
        keywords = obj.keywords.all()
        keyword_list = []
        for keyword in keywords:
            keyword_list.append(keyword.name)
        return keyword_list


# ================= Movie Serializer =================== #
class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField('getGenre')
    production_companies = serializers.SerializerMethodField('getCompany')
    production_countries = serializers.SerializerMethodField('getCountry')
    spoken_languages = serializers.SerializerMethodField('getLanguage')
    keywords = serializers.SerializerMethodField('getKeyword')

    class Meta:
        model = Movie
        fields = (
            'id',
            'adult',
            'collection',
            'budget',
            'genres',
            'homepage',
            'original_language',
            'original_title',
            'overview',
            'popularity',
            'poster_path',
            'backdrop_path',
            'production_companies',
            'production_countries',
            'release_date',
            'revenue',
            'runtime',
            'spoken_languages',
            'status',
            'tagline',
            'title',
            'video',
            'vote_average',
            'vote_count',
            'keywords',
            'view_cnt'
        )

    def getGenre(self, obj):
        genres = obj.genres.all()
        genre_list = []
        for genre in genres:
            genre_list.append(genre.name)
        return genre_list

    def getCompany(self, obj):
        companies = obj.production_companies.all()
        company_list = []
        for company in companies:
            company_list.append(company.name)
        return company_list

    def getCountry(self, obj):
        countries = obj.production_countries.all()
        country_list = []
        for country in countries:
            country_list.append(country.name)
        return country_list

    def getLanguage(self, obj):
        languages = obj.spoken_languages.all()
        language_list = []
        for language in languages:
            language_list.append(language.name)
        return language_list

    def getKeyword(self, obj):
        keywords = obj.keywords.all()
        keyword_list = []
        for keyword in keywords:
            keyword_list.append(keyword.name)
        return keyword_list

# class SimilarMovieSerializer(serializers.ModelSerializer):
#     movie_info = serializers.SerializerMethodField('get_movie_info')

#     class Meta:
#         model = MovieCluster
#         fields = ('movie', 'cluster','movie_info')

#     def get_movie_info(self, obj):
#         movie={'id':obj.movie.id, 'title':obj.movie.title,'genres':obj.movie.genres,'view_cnt':obj.movie.view_cnt,'poster_path':obj.movie.poster_path,'backdrop_path':obj.movie.backdrop_path,
#         'overview':obj.movie.overview,'runtime':obj.movie.runtime,'video_url':obj.movie.video_url,'adult':obj.movie.adult,}
#         return movie


class MovieAgeSerializer(serializers.ModelSerializer):
    genres_array = serializers.ReadOnlyField()
    user_age = serializers.SerializerMethodField('getWatchedUser')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres_array', 'view_cnt', 'user_age')

    def getWatchedUser(self, obj):
        movies = Rating.objects.filter(movie=obj)
        age_dict = {}

        for watched in movies:
            if watched.user.profile.age not in age_dict.keys():
                age_dict[watched.user.profile.age] = 1
            else:
                age_dict[watched.user.profile.age] += 1

        return age_dict


class MovieGenderSerializer(serializers.ModelSerializer):
    genres_array = serializers.ReadOnlyField()
    user_gender = serializers.SerializerMethodField('getWatchedUser')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres_array', 'view_cnt', 'user_gender')

    def getWatchedUser(self, obj):
        movies = Rating.objects.filter(movie=obj)
        gender_dict = {}

        for watched in movies:
            if watched.user.profile.gender not in gender_dict.keys():
                gender_dict[watched.user.profile.gender] = 1
            else:
                gender_dict[watched.user.profile.gender] += 1

        return gender_dict

class CrewSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Crew
        fields = ('id', 'movie', 'department', 'profile_path', 'gender', 'name', 'job')

# ================= Rating Serializer =================== #
class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('user', 'movie', 'rating', 'timestamp')


class UserRatingSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_movie_id')
    title = serializers.SerializerMethodField('get_movie_title')
    release_date = serializers.SerializerMethodField('get_release_date')
    poster_path = serializers.SerializerMethodField('get_poster_path')

    class Meta:
        model = Rating
        fields = ('user', 'id', 'title', 'release_date', 'rating', 'timestamp', 'poster_path')

    def get_movie_id(self, obj):
        return obj.movie.id

    def get_movie_title(self, obj):
        return obj.movie.title

    def get_release_date(self, obj):
        return obj.movie.release_date

    def get_poster_path(self, obj):
        return obj.movie.poster_path


class SessionSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField('get_email')
    username = serializers.SerializerMethodField('get_user')
    token = serializers.SerializerMethodField('get_token')
    gender = serializers.SerializerMethodField('get_gender')
    age = serializers.SerializerMethodField('get_age')
    occupation = serializers.SerializerMethodField('get_occupation')
    is_auth = serializers.SerializerMethodField('get_is_auth')
    is_staff = serializers.SerializerMethodField('get_is_staff')
    movie_taste = serializers.SerializerMethodField('get_movie_taste')

    class Meta:
        model = Profile
        fields = ('email', 'username', 'token', 'gender', 'age', 'occupation', 'is_auth', 'is_staff', 'movie_taste')

    def get_email(self, obj):
        return str(obj['email'])

    def get_user(self, obj):
        return str(obj['username'])

    def get_token(self, obj):
        return str(obj['token'])

    def get_is_auth(self, obj):
        return obj['is_auth']

    def get_is_staff(self, obj):
        return obj['is_staff']

    def get_movie_taste(self, obj):
        return obj['movie_taste']

    def get_gender(self, obj):
        return obj['gender']

    def get_age(self, obj):
        return obj['age']

    def get_occupation(self, obj):
        return obj['occupation']
