from django.urls import path
from . import views

urlpatterns = [
    path('getmovie/', views.getMovie),
    path('createmovie/', views.createMovie),
]
