from rest_framework.response import Response
from rest_framework.decorators import api_view

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import ArticleListSerializer, ArticleSerializer, ArticleCommentSerializer
from .models import Article, ArticleComment


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        page = int(request.GET.get('page'))
        articles = Article.objects.all().order_by('-created_at')
        res_article = []
        for i in range((page-1)*10, page*10):
            if i < len(articles):
                res_article.append(articles[i])
        serializer = ArticleListSerializer(res_article, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        # 처음 불러올 때도 이 게시글을 좋아하는지에 대한 정보가 필요함
        if article.like_users.filter(pk=request.user.pk).exists():
            isLiking = True
        else:
            isLiking = False
        data = {
            'article': serializer.data,
            'isLiking': isLiking,
        }
        return Response(data)
    
    elif request.method == 'DELETE':
        if article.user == request.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        if article.user == request.user:
            serializer = ArticleSerializer(article, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list(request, article_pk):
    if request.method == 'GET':
        comments = get_list_or_404(ArticleComment, article_id=article_pk)
        serializer = ArticleCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=article_pk)
        serializer = ArticleCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(ArticleComment, pk=comment_pk)

    if request.method == 'GET':
        serializer = ArticleCommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if comment.user == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        if comment.user == request.user:
            serializer = ArticleCommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likes(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.like_users.filter(pk=request.user.pk).exists():
        article.like_users.remove(request.user)
        isLiking = False
    else:
        article.like_users.add(request.user)
        isLiking = True
    data = {
        'isLiking': isLiking,
    }
    return Response(data)

    
