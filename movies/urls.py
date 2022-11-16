from django.urls import path
from . import views

urlpatterns = [
    path('makefixtures/', views.makeFixtures),
    path('createmovie/', views.createMovie),
]
