from django.urls import path
from . import views

urlpatterns = [
    # path('makefixtures/', views.makeFixtures),
    # path('movies/', views.movie_list),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('movies/popular/init/', views.popular_movie_init),
    path('movies/popular/<int:page>/', views.popular_movie_list),
    path('actors/<int:actor_pk>/', views.actor_detail),
    path('movies/<int:movie_pk>/comments/', views.comment_create),
    path('comments/<int:comment_pk>/', views.comment_detail),
]
