from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import requests
from .models import Movie
from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view

from .serializers import MovieSerializer

@api_view(['GET'])
# Create your views here.
def getMovie(request):
    # top_rated movies api request
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

        # return Response(serializer.data, status=status.HTTP_201_CREATED)

    # queryset to json
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)

    # with open(r'merged.json', 'w', encoding="UTF-8") as merged_file:
    #     merged_file.write(movies_json)

    return Response(serializer.data)

    return render(request, 'movies/getmovie.html')

def createMovie(request):
    return 