from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from .forms import UserForm
from .serializers import ProfileSerializer

from collections import defaultdict


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, user_pk):
    User = get_user_model()
    me = request.user
    profile_user = User.objects.get(pk=user_pk)

    # 잔디용 데이터 =========================================================
    acts_dic = defaultdict(int)
    acts_total_cnt = 0

    # 게시글 수 카운트
    for article in profile_user.article_set.all():
        date = str(article.created_at)[:10]
        acts_dic[date] += 1
        acts_total_cnt += 1

    # 게시글 댓글 수 카운트
    for articlecomment in profile_user.articlecomment_set.all():
        date = str(articlecomment.created_at)[:10]
        acts_dic[date] += 1
        acts_total_cnt += 1
    
    # 영화 댓글 수 카운트
    for moviecomment in profile_user.comment_set.all():
        date = str(moviecomment.created_at)[:10]
        acts_dic[date] += 1
        acts_total_cnt += 1

    acts = []  # 활동 정보
    for d, c in acts_dic.items():
        act_dic = {
            'date': d,
            'count': c
        }
        acts.append(act_dic)
    # ========================================================================

    serializer = ProfileSerializer(profile_user)
    data = {
        'user': serializer.data,
        'acts': acts,
        'acts_total_cnt': acts_total_cnt
    }

    if me != profile_user:
        if profile_user.followers.filter(pk=me.pk).exists():
            isFollowing = True
        else:
            isFollowing = False
        data['isFollowing'] = isFollowing

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_image(request, user_pk):
    User = get_user_model()
    me = request.user
    profile_user = User.objects.get(pk=user_pk)
    if me == profile_user:
        form = UserForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid():
            form = form.save(commit=False)
            form.profile_image_url = request.FILES.get('image')
            form.save()
        serializer = ProfileSerializer(profile_user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    User = get_user_model()
    me = request.user
    profile_user = User.objects.get(pk=user_pk)
    if me != profile_user:
        if profile_user.followers.filter(pk=me.pk).exists():
            profile_user.followers.remove(me)
            isFollowing = False
        else:
            profile_user.followers.add(me)
            isFollowing = True
        data = {
            'isFollowing': isFollowing
        }
        return Response(data)
    