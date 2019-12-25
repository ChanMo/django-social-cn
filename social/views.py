from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from .models import *


class AuthView(View):
    """
    第三方登录
    """
    success_url = '/accounts/profile/'

    def get_success_url(self):
        return self.success_url

    def get(self, request, *args, **kwargs):
        pro = get_object_or_404(Provider, name=kwargs['provider'])
        code = request.GET.get('code', None)

        if not code:
            url = pro.get_auth_url(request)

            return HttpResponseRedirect(url)
        uid = pro.get_uid(request, code)
        user = Social.objects.auth_user(pro, uid)
        login(request, user)

        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)
