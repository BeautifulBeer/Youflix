from django.contrib import admin
from .models import Profile, Movie, Rating
from .models import Genre,Collection,Company,Keyword,Cast,Crew,Language,UserCluster
from import_export.admin import ImportExportModelAdmin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
         (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)

@admin.register(Movie)
class MovieAdmin(ImportExportModelAdmin):
    list_display=('id','title','release_date','kmeans_cluster',)

@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    list_display=('id','name',)

@admin.register(Collection)
class CollectionAdmin(ImportExportModelAdmin):
    list_display=('id','name','poster_path','backdrop_path',)

@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    list_display=('id','name',)

@admin.register(Keyword)
class KeywordAdmin(ImportExportModelAdmin):
    list_display=('id','name',)

@admin.register(Cast)
class CastAdmin(ImportExportModelAdmin):
    list_display=('id','movie','character','profile_path','gender','name','order',)

@admin.register(Crew)
class CrewAdmin(ImportExportModelAdmin):
    list_display=('id','movie','department','profile_path','gender','name','job',)

@admin.register(Language)
class LanguageAdmin(ImportExportModelAdmin):
    list_display=('iso','name',)

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    list_display=('pk','id','user','username','gender','age','occupation','movie_taste','kmeans_cluster',)

@admin.register(Rating)
class RatingAdmin(ImportExportModelAdmin):
    list_display=('user','movie','rating','timestamp',)

@admin.register(UserCluster)
class UserClusterAdmin(ImportExportModelAdmin):
    list_display=('user_id','kmeans_cluster',)