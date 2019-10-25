import datetime

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

# ============= Django User 사용자 정의 ============== #


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=10, blank=False)
    gender = models.CharField(max_length=10, default='M')
    age = models.IntegerField(default=25)
    occupation = models.CharField(max_length=200)
    movie_taste = models.TextField(null=True)
    kmeans_cluster = models.IntegerField(null=True)


#  wrapper for create user Profile
def create_profile(**kwargs):

    user = User.objects.create_user(
        id=kwargs['id'],
        email=kwargs['email'],
        password=kwargs['password'],
        is_active=True,
    )
    try:
        profile = Profile.objects.create(
            id=kwargs['id'],
            user=user,
            username=kwargs['username'],
            gender=kwargs['gender'],
            age=kwargs['age'],
            occupation=kwargs['occupation'],
            movie_taste=kwargs['movie_taste']
        )
    except:
        profile = Profile.objects.create(
            id=kwargs['id'],
            user=user,
            username=kwargs['username'],
            gender=kwargs['gender'],
            age=kwargs['age'],
            occupation=kwargs['occupation'],
        )

    return profile


# ============= Django User 사용자 정의 ============== #
class Collection(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    poster_path = models.TextField(default='')
    backdrop_path = models.TextField(default='')

    def __str__(self):
        return self.name


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Country(models.Model):
    iso = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Language(models.Model):
    iso = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Link(models.Model):
    tmdbid = models.IntegerField()
    movieid = models.IntegerField()
    imdbid = models.CharField(max_length=100)


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=100)
    adult = models.BooleanField()
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True)
    budget = models.IntegerField(default=0)
    genres = models.ManyToManyField(Genre, related_name='movies')
    homepage = models.TextField(default='')
    original_language = models.CharField(max_length=10, default='')
    original_title = models.CharField(max_length=200, default='')
    overview = models.TextField(default='')
    popularity = models.FloatField(default=0, null=True)
    poster_path = models.TextField(default='')
    backdrop_path = models.TextField(default='')
    production_companies = models.ManyToManyField(Company, related_name='movies')
    production_countries = models.ManyToManyField(Country, related_name='movies')
    release_date = models.DateField(null=True)
    revenue = models.FloatField(default=0, null=True)
    runtime = models.IntegerField(default=0, null=True)
    spoken_languages = models.ManyToManyField(Language, related_name='movies')
    status = models.CharField(max_length=50, null=True)
    tagline = models.TextField(default='', null=True)
    title = models.CharField(max_length=200, default='')
    video = models.TextField(null=True)
    vote_average = models.FloatField(default=0, null=True)
    vote_count = models.IntegerField(default=0, null=True)
    keywords = models.ManyToManyField(Keyword, related_name='movies')
    view_cnt = models.IntegerField(default=0)
    kmeans_cluster = models.IntegerField(null=True)

    @property
    def genres_array(self):
        return self.genres.strip().split('|')


class Cast(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    character = models.CharField(max_length=100, null=True)
    profile_path = models.TextField(default='')
    gender = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=50, null=True)
    order = models.IntegerField()


class Crew(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, null=True)
    profile_path = models.TextField(default='')
    gender = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=50, null=True)
    job = models.CharField(max_length=50, null=True)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()
    timestamp = models.DateTimeField()


class Comment(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField()


# Cluster Model
class UserCluster(models.Model):
    user_id = models.IntegerField(primary_key=True)
    kmeans_cluster = models.IntegerField(blank=True)

# class MovieCluster(models.Model):
#     movie_id=models.IntegerField(primary_key=True)
#     kmeans_cluster=models.IntegerField(blank=True)
