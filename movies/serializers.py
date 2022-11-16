from rest_framework import serializers
from .models import Movie


# get_movie_title
class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'



