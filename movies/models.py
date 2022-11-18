from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)


class Actor(models.Model):
    actor_id = models.IntegerField(primary_key=True)
    gender = models.IntegerField()
    name = models.CharField(max_length=100)
    original_name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=200, null=True)


class Movie(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=200, blank=True)
    video_path = models.CharField(max_length=200, blank=True)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)