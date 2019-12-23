import logging
import uuid

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from .serializers import *
from .signals import social_auth_done

logger = logging.getLogger(__name__)


class AuthView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None, **kwargs):
        pro = get_object_or_404(Provider, name=kwargs['provider'])
        code = request.GET.get('code', None)
        try:
            auth_result = pro.get_uid(request, code)
            uid = auth_result['openid']
        except Exception as e:
            logger.warning(e)

            return Response({'detail':'授权失败'},
                    status=status.HTTP_400_BAD_REQUEST)

        if Social.objects.filter(provider=pro, uid=uid).exists():
            social = Social.objects.get(provider=pro, uid=uid)
            user = social.user
        else:
            User = get_user_model()

            username = str(uuid.uuid4())[:8]

            while User.objects.filter(username=username).exists():
                username = str(uuid.uuid4())[:8]
            user = User.objects.create_user(username)
            so = Social.objects.create(provider=pro, uid=uid, user=user)
            social_auth_done.send(sender=self.__class__, so=so)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        })


class SocialUpdateView(UpdateAPIView):
    serializer_class = SocialSerializer

    def get_object(self):
        return self.request.user.social_set.first()
