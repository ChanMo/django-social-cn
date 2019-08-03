import json
import random
import string
import urllib.request

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Provider(models.Model):
    name = models.CharField(_('name'), max_length=200)
    code = models.CharField(_('code'), max_length=50, unique=True)
    url = models.URLField(_('url'))
    appid = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('provider')
        verbose_name_plural = _('provider')


def _random_str():
    " 生成随机字符串 "

    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))


def _generate_username():
    " 随机生成用户名 "
    username = _random_str()

    while User.objects.filter(username=username).exists():
        username = _random_str()

    return username


class SocialManager(models.Manager):
    def get_or_create_user(self, uid, provider, data):
        " 获取或创建用户 "
        try:
            if provider.code in ['wxa', 'wechat']:
                obj = Social.objects.get(uid=uid,
                        provider__code__in=['wxa', 'wechat'])
            else:
                obj = Social.objects.get(uid=uid, provider=provider)
            created = False
        except:
            obj = Social.objects.create_user(uid, provider)
            created = True
        obj.extra_data = data
        obj.save()

        return created, obj


    def create_user(self, uid, provider):
        " 创建用户 "
        username = _generate_username()
        user = User.objects.create_user(username, '', '')

        return Social.objects.create(user=user, uid=uid, provider=provider)

    def fetch_auth(self, provider_code, code, p):
        """
        获取Auth UID
        p: 推广人ID
        """
        try:
            provider = Provider.objects.get(code=provider_code)
        except:
            return False, "provider不存在"

        url = provider.url % (provider.appid, provider.secret, code)
        with urllib.request.urlopen(url) as f:
            result = f.read().decode('utf8')
            result = json.loads(result)

        if result.get('unionid'):
            uid = result.get('unionid')
        elif result.get('openid'):
            uid = result.get('openid')
        else:
            return False, result['errmsg']
        created, obj = Social.objects.get_or_create_user(uid, provider, result)


        return True, obj


class Social(models.Model):
    """ 第三方登录 """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
            verbose_name=_('user'))
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE,
            verbose_name=_('provider'))
    uid = models.CharField(_('uid'), max_length=200)
    extra_data = JSONField(_('extra date'), blank=True, null=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    objects = SocialManager()

    def __str__(self):
        return self.user.username


    class Meta:
        ordering = ['-created']
        unique_together = ['provider', 'uid']
        verbose_name = _('social')
        verbose_name_plural = _('social')
