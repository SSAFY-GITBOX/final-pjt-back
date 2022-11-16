from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Movie, Genre, Actor
from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .serializers import MovieSerializer, ActorSerializer


@api_view(['GET'])
def makeFixtures(request):
    # # 1. Top Rated Movies API request ===================================================================
    # for page in range(1, 51):
    #     response = requests.get(f'https://api.themoviedb.org/3/movie/top_rated?api_key=8d8e9b9672f4d1a183be6806ad451223&language=ko-KR&page={page}')
    #     if response.status_code == 200:
    #         for result in response.json()['results']:
    #             res = requests.get(f"https://api.themoviedb.org/3/movie/{result['id']}/videos?api_key=8d8e9b9672f4d1a183be6806ad451223&language=ko-KR")
    #             if res.status_code == 200:
    #                 if len(res.json()['results']) != 0:
    #                     result['video_path'] = res.json().get('results')[0].get('key')
    #                 result['genres'] = result['genre_ids']
    #                 result['movie_id'] = result['id']
    #                 serializer = MovieSerializer(data=result)
    #                 if serializer.is_valid(raise_exception=True):
    #                     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # # 2. Actor API request ===============================================================================
    # movies = Movie.objects.all()
    # serializer = MovieSerializer(movies, many=True)
    # for movie in list(movies):
    #     res = requests.get(f"https://api.themoviedb.org/3/movie/{movie.movie_id}/credits?api_key=8d8e9b9672f4d1a183be6806ad451223&language=ko-KR")
    #     count = 0
    #     for actor in res.json()['cast']:
    #         if Actor.objects.filter(pk=actor['id']).exists():
    #             pass
    #         else:     
    #             tmp = Actor()
    #             tmp.actor_id = actor['id']
    #             tmp.gender = actor['gender']
    #             tmp.name = actor['name']
    #             tmp.original_name = actor['original_name']
    #             tmp.profile_path = actor['profile_path']
    #             tmp.save()
    #         count += 1
    #         if count == 3:
    #             break

    # # 3. Actor - Movie N:M 관계 설정 ======================================================================
    # movies = Movie.objects.all()
    # for movie in movies:
    #     res = requests.get(f"https://api.themoviedb.org/3/movie/{movie.movie_id}/credits?api_key=8d8e9b9672f4d1a183be6806ad451223&language=ko-KR")
    #     if res.status_code == 200:
    #         count = 0
    #         for cast in res.json()['cast']:
    #             actor = Actor.objects.get(pk=cast['id'])
    #             movie.actors.add(actor)
    #             count += 1
    #             if count == 3:
    #                 break

    # # 4. Query to Json =====================================================================================
    # movies = Movie.objects.all()
    # movies_json = serializers.serialize('json', movies)
    # with open(r'movies.json', 'w', encoding="UTF-8") as movies_file:
    #     movies_file.write(movies_json)

    # genres = Genre.objects.all()
    # genres_json = serializers.serialize('json', genres)
    # with open(r'genres.json', 'w', encoding="UTF-8") as genres_file:
    #     genres_file.write(genres_json)

    # actors = Actor.objects.all()
    # actors_json = serializers.serialize('json', actors)
    # with open(r'actors.json', 'w', encoding="UTF-8") as actors_file:
    #     actors_file.write(actors_json)
    return
