from django.urls import path
from . import views

urlpatterns = [
    # path('makefixtures/', views.makeFixtures),
    path('movies/', views.movie_list),
    path('movies/popular/init/', views.popular_movie_init),
    path('movies/popular/<int:page>/', views.popular_movie_list),
]
