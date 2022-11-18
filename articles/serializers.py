from rest_framework import serializers
from .models import Article, ArticleComment


class ArticleListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'user', 'username')
        read_only_fields = ('like_users',)


class ArticleCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ArticleComment
        fields = '__all__'
        read_only_fields = ('article', 'user',)


class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    articlecomment_set = ArticleCommentSerializer(many=True, read_only=True)
    articlecomment_count = serializers.IntegerField(source='articlecomment_set.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'like_users',)
