from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User
from articles.serializers import ArticleListSerializer, ArticleCommentSerializer
from movies.serializers import MovieSerializer, CommentSerializer


class UserSerializer(serializers.ModelSerializer):
    User = get_user_model()

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    User = get_user_model()
    followers = UserSerializer(many=True, read_only=True)
    followers_cnt = serializers.IntegerField(source='followers.count', read_only=True)
    followings = UserSerializer(many=True, read_only=True)
    followings_cnt = serializers.IntegerField(source='followings.count', read_only=True)
    like_articles = ArticleListSerializer(many=True, read_only=True)
    article_set = ArticleListSerializer(many=True, read_only=True)
    articlecomment_set = ArticleCommentSerializer(many=True, read_only=True)
    like_movies = MovieSerializer(many=True, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('profile_image',)
        