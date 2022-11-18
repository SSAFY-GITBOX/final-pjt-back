from django.shortcuts import render

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, Http404

from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Movie, Genre, Actor, Comment
from .serializers import MovieSerializer, MovieListSerializer
from .serializers import GenreListSerializer, ActorSerializer, CommentSerializer

# Create your views here.

# 영화 전체 조회 없어도 될듯?
# @api_view(['GET'])
# def movie_list(request):
#     movies = get_list_or_404(Movie)
#     serializer = MovieSerializer(movies, many=True)
#     return Response(serializer.data)


# 인기 영화 전체보기 클릭시 1~34페이지 까지, 35페이지 이상 요청할 시 에러 구현해야함
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def popular_movie_list(request):
    movies = get_list_or_404(Movie)
    res_movies = []
    page = request.GET.get('page', None)
    if page == None:
        for i in range(0, 30):
            res_movies.append(movies[i])
    else:
        if page != '0' and page.isdigit():
            for i in range((int(page)-1)*30, int(page)*30):
                if i < len(movies):
                    res_movies.append(movies[i])

    if res_movies:
        serializer = MovieListSerializer(res_movies, many=True)
        return Response(serializer.data)
    else:
        raise Http404("Question does not exist")


# 모든 장르 조회
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def genre_list(request):
    genres = get_list_or_404(Genre)
    serializers = GenreListSerializer(genres, many=True)
    return Response(serializers.data)


# 장르 선택 초기 요청
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def genre_movie_init(request, genre_id):
    movies = Movie.objects.filter(genres=genre_id).order_by('-vote_count')
    init_movies = []
    for i in range(0, 20):
        if i < len(movies):
            init_movies.append(movies[i])

    serializer = MovieListSerializer(init_movies, many=True)
    context = {
        'movies': serializer.data,
        'movie_length': len(movies)
    }
    return Response(context)

# 장르별 영화 조회
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def genre_movie_list(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = Movie.objects.filter(genres=genre)
    res_movies = []
    page = request.GET.get('page', None)
    if page == None:
        for i in range(0, 30):
            res_movies.append(movies[i])
    else:
        if page != '0' and page.isdigit():
            for i in range((int(page)-1)*30, int(page)*30):
                if i < len(movies):
                    res_movies.append(movies[i])

    if res_movies:
        serializer = MovieListSerializer(res_movies, many=True)
        return Response(serializer.data)
    else:
        raise Http404("Question does not exist")


# 홈 화면에 노출될 인기영화 초기 요청
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def popular_movie_init(request):
    movies = get_list_or_404(Movie)
    page_movies = []
    for i in range(0, 20):
        page_movies.append(movies[i])
    serializer = MovieListSerializer(page_movies, many=True)
    return Response(serializer.data)


# movie detail GET 요청
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# actor detail GET 요청
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def actor_detail(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)
    serializer = ActorSerializer(actor)
    return Response(serializer.data)


# 영화 코멘트 생성 요청
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def comment_create(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 영화 코멘트 조회, 수정, 삭제
@permission_classes([IsAuthenticated])
@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET'])
# def makeFixtures(request):
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
    # movies = Movie.objects.all().order_by('-vote_count')
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
    # return

