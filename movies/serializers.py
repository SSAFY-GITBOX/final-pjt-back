from rest_framework import serializers
from .models import Movie, Actor, Comment


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('movie_id', 'poster_path',)


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('movie',)


class MovieSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_rating_avg = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_comment_rating_avg(self, obj):
        total = 0
        for comment in obj.comment_set.all():
            total += comment.rating
        return total / len(obj.comment_set.all())