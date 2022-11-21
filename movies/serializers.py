from rest_framework import serializers
from .models import Movie, Actor, Comment, Genre


class SearchedMovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('movie_id', 'poster_path', 'title', 'overview', 'genres')

class GenreListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('movie_id', 'poster_path',)
        read_only_fields = ('like_users',)


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('movie', 'user', )


class MovieSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_rating_avg = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('like_users',)

    def get_comment_rating_avg(self, obj):
        total = 0
        if len(obj.comment_set.all()) == 0:
            return 0
        else:
            for comment in obj.comment_set.all():
                total += comment.rating
            return total / len(obj.comment_set.all())