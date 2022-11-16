from django.urls import path
from . import views

urlpatterns = [
    # path('makefixtures/', views.makeFixtures),
    path('movies/', views.movie_list),
    path('movies/popular/<int:page>/', views.movie_popular_list),
]
