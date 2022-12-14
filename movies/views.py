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
from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Movie, Genre, Actor, Comment
from .serializers import MovieSerializer, MovieListSerializer, SearchedMovieListSerializer
from .serializers import GenreListSerializer, ActorSerializer, CommentSerializer
from accounts.serializers import forRecommendUserSerializer

from collections import defaultdict
import random


# import requests

# Create your views here.

# 영화 전체 조회 없어도 될듯?
# @api_view(['GET'])
# def movie_list(request):
#     movies = get_list_or_404(Movie)
#     serializer = MovieSerializer(movies, many=True)
#     return Response(serializer.data)

# 네브바 - 검색 결과 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_movie(request):
    searched_title = request.GET.get('content', None)
    movies = Movie.objects.filter(title__contains=searched_title)
    serializer = SearchedMovieListSerializer(movies, many=True)
    return Response(serializer.data)


# 모든 장르 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genre_list(request):
    genres = get_list_or_404(Genre)
    serializers = GenreListSerializer(genres, many=True)
    return Response(serializers.data)


# 홈 - 최신영화 초기 요청
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def latest_movie_init(request):
    movies = get_list_or_404(Movie.objects.order_by('-release_date'))
    init_movies = []
    for i in range(0, 100):
        init_movies.append(movies[i])
    serializer = MovieListSerializer(init_movies, many=True)

    context = {
        'movies': serializer.data,
        'movie_length': len(movies)
    }
    return Response(context)


# 최신 영화 전체 보기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def latest_movie_list(request):
    movies = get_list_or_404(Movie.objects.order_by('-release_date'))
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


# 홈 - 장르별 영화 초기 요청
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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


# 장르별 영화 전체 보기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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


# movie detail GET 요청
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    # 처음 불러올 때도 이 영화를 좋아하는지에 대한 정보가 필요함
    if movie.like_users.filter(pk=request.user.pk).exists():
        isLiking = True
    else:
        isLiking = False
    data = {
        'movie': serializer.data,
        'isLiking': isLiking
    }
    return Response(data)


# 영화 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_likes(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        isLiking = False
    else:
        movie.like_users.add(request.user)
        isLiking = True
    context = {
        'isLiking': isLiking,
    }
    return Response(context)


# actor detail GET 요청
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def actor_detail(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)
    serializer = ActorSerializer(actor)
    return Response(serializer.data)


# 영화 코멘트 생성 요청
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 영화 코멘트 조회, 수정, 삭제
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if comment.user == request.user:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

    elif request.method == 'DELETE':
        if comment.user == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


# 추천 영화 장르 별 개수
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def recommend(request, user_pk):
    User = get_user_model()
    me = User.objects.get(pk=user_pk)
    follow_cnt = len(me.followings.all())
    genreScoreForChart = dict()
    all_genres = Genre.objects.all()
    for genre in all_genres:
        genreScoreForChart[genre.name] = 0
    # 내 점수 반영
    my_visited = defaultdict(float)  # 내 영화 방문 체크 용
    # 내 장르 점수 계산
    genreScore = defaultdict(float)
    # 내 댓글 평점 반영
    for comment in me.comment_set.all():
        # 같은 영화의 댓글 중복 계산 방지 (먼저 단 댓글이 반영 됨)
        if my_visited[str(comment.movie_id)]:
            continue
        my_visited[str(comment.movie_id)] = 1  # 방문 체크
        # 해당 댓글을 남긴 영화
        movie = Movie.objects.get(pk=comment.movie_id)
        sign = comment.rating - 5  # 계산에 쓸 부호
        if sign > 0:
            sign = 1
        elif sign < 0:
            sign = -1
        score = (comment.rating - 5) // 2 + sign  # 댓글 평점 점수
        for genre in movie.genres.all():
            genreScore[str(genre.id)] += float(score)
            genreScoreForChart[str(genre.name)] += float(score)
    # 내 좋아요 반영
    for movie in me.like_movies.all():
        # 평점을 매겼던 영화는 좋아요 점수 반영 안함
        if my_visited[str(movie.pk)]:
            continue
        for genre in movie.genres.all():
            genreScore[str(genre.id)] += 2.0
            genreScoreForChart[str(genre.name)] += 2.0
    if follow_cnt:
        # 팔로우 유저들 점수 반영
        yourGenreScore = defaultdict(float)  # 팔로우 유저들의 점수 합 (나중에 평균화)
        yourGenreScoreForChart = dict()
        for genre in all_genres:
            yourGenreScoreForChart[genre.name] = 0
        for you in me.followings.all():
            visited = defaultdict(float)  # 영화 방문 체크 용
            # 장르 점수 계산
            # 팔로우 유저 댓글 평점 반영
            for comment in you.comment_set.all():
                # 같은 영화의 댓글 중복 계산 방지 (먼저 단 댓글이 반영 됨)
                if visited[str(comment.movie_id)]:
                    continue
                visited[str(comment.movie_id)] = 1  # 방문 체크
                # 해당 댓글을 남긴 영화
                movie = Movie.objects.get(pk=comment.movie_id)
                sign = comment.rating - 5  # 계산에 쓸 부호
                if sign > 0:
                    sign = 1
                elif sign < 0:
                    sign = -1
                score = (comment.rating - 5) // 2 + sign  # 댓글 평점 점수
                for genre in movie.genres.all():
                    yourGenreScore[str(genre.id)] += float(score)
                    yourGenreScoreForChart[str(genre.name)] += float(score)
            # 팔로우 유저 좋아요 반영
            for movie in you.like_movies.all():
                # 평점을 매겼던 영화는 좋아요 점수 반영 안함
                if visited[str(movie.pk)]:
                    continue
                for genre in movie.genres.all():
                    yourGenreScore[str(genre.id)] += 2.0
                    yourGenreScoreForChart[str(genre.name)] += 2.0
        # 팔로우 유저 점수 평균화
        for key, value in yourGenreScore.items():
            genreScore[key] += value / float(follow_cnt)  # 평균화해서 기존 스코어에 더함
        for key, value in yourGenreScoreForChart.items():
            genreScoreForChart[key] += value / float(follow_cnt)
    for key, value in genreScoreForChart.items():  # 차트용 데이터에 음수 값은 굳이 필요 없음
        if value < 0:
            genreScoreForChart[key] = 0
    # 장르별 랜덤으로 뽑을 개수 구하기
    scoreSum = sum(list(genreScore.values()))
    genreCnt = defaultdict(int)
    for key, value in genreScore.items():
        if value <= 0:
            continue
        genre_cnt = int(15 * (value / scoreSum))
        if genre_cnt == 0:
            continue
        genreCnt[key] = genre_cnt
    # 추천 영화 리스트에 무비 오브젝트 넣기 
    recommend_cnt = 0
    recommended_movies = []
    genreCnt = dict(sorted(genreCnt.items(), key=lambda x: x[1], reverse=True))  # 카운트 많은 순으로 정렬
    for key, cnt in genreCnt.items():  
        genre = Genre.objects.get(pk=key)
        recommended_movies += random.choices(genre.movie_set.all(), k=cnt)
        recommend_cnt += cnt
        if recommend_cnt >= 10:
            break
    recommended_movies = list(set(sorted(recommended_movies, key=lambda x: x.vote_count, reverse=True)))  # 중복 제거, 평가 수를 기준으로 내림차순 정렬
    recommend_serializer = MovieSerializer(recommended_movies, many=True)
    # 기본으로 제공하는 랜덤 무비 5개
    random_movies = list(random.choices(Movie.objects.all(), k=5))
    random_movies = list(set(sorted(random_movies, key=lambda x: x.vote_count, reverse=True)))  # 중복 제거, 평가 수를 기준으로 내림차순 정렬
    for idx, random_movie in enumerate(random_movies):  # 추천 영화에 있는 랜덤 영화 중복 제거
        for recommended_movie in recommended_movies:
            if random_movie.pk == recommended_movie.pk:
                del random_movies[idx]
                break
    random_serializer = MovieSerializer(random_movies, many=True)
    data = {
        'genreScore': genreScoreForChart,
        'recommended': recommend_serializer.data,
        'random': random_serializer.data,
    }
    return Response(data)


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
    #         if count == 10:
    #             break

    # 3. Actor - Movie N:M 관계 설정 ======================================================================
    # movies = Movie.objects.all()
    # for movie in movies:
    #     res = requests.get(f"https://api.themoviedb.org/3/movie/{movie.movie_id}/credits?api_key=8d8e9b9672f4d1a183be6806ad451223&language=ko-KR")
    #     if res.status_code == 200:
    #         count = 0
    #         for cast in res.json()['cast']:
    #             try:
    #                 actor = Actor.objects.get(pk=cast['id'])
    #                 movie.actors.add(actor)
    #                 count += 1
    #                 if count == 10:
    #                     break
    #             except:
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
    # return Response(actors_json.data)
