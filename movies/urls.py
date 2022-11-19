from django.urls import path
from . import views

urlpatterns = [
    # path('makefixtures/', views.makeFixtures),
    # path('movies/', views.movie_list),
    path('genres/', views.genre_list),
    path('movies/latest/init/', views.latest_movie_init),
    path('movies/latest/', views.latest_movie_list),
    path('movies/genres/<int:genre_id>/init/', views.genre_movie_init),
    path('movies/genres/<int:genre_id>', views.genre_movie_list),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('movies/<int:movie_pk>/likes/', views.movie_likes),
    path('actors/<int:actor_pk>/', views.actor_detail),
    path('movies/<int:movie_pk>/comments/', views.comment_create),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('movies/search', views.search_movie),
]
