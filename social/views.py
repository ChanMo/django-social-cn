from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import *


@api_view(['GET'])
@permission_classes((AllowAny,))
def auth_view(request, provider):
    code = request.GET.get('code', '')
    p = request.GET.get('p', 0)

    if not code:
        return Response({'detail':'code参数不存在'},
                status=status.HTTP_400_BAD_REQUEST)
    success, obj = Social.objects.fetch_auth(provider, code, p)

    if success:
        return Response({'detail': obj.user.auth_token.key, 'mobile':obj.user.member.mobile})
    else:
        return Response({'detail': obj},
                status=status.HTTP_400_BAD_REQUEST)
