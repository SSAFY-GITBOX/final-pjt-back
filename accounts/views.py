from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from .serializers import UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_image(request, user_pk):
    User = get_user_model()
    profile_user = User.objects.get(pk=user_pk)
    if request.user == profile_user:
        profile_user.profile_image = request.data['profile_image']
        profile_user = profile_user.save()
        serializer = UserSerializer(profile_user)
        return Response(serializer.data)
