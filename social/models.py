import json
import logging
import urllib.request

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class Provider(models.Model):
    NAME_CHOICES = (
            ('wxa', _('wxa')),
            ('wxb', _('wechat web')),
            ('wechat', _('wechat open')),
            ('qq', _('qq open')),
            ('douyin', _('douyin'))
            )
    name = models.CharField(_('name'), max_length=200, choices=NAME_CHOICES)
    appid = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_name_display()

    def get_auth_url(self, request):
        " 获取授权请求地址(仅web端需要) "
        redirect_uri = 'https://%s%s' % (request.site.domain, request.path)

        if self.name == 'wechat':
            url = 'https://open.weixin.qq.com/connect/qrconnect?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect' % (self.appid, redirect_uri)
        elif self.name == 'qq':
            redirect_uri = 'https://%s/social/auth/qq' % request.site.domain
            url = 'https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=%s&redirect_uri=%s&state=STATE' % (self.appid, redirect_uri)
        elif self.name == 'wxb':
            url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope={}&state=STATE#wechat_redirect'.format(self.appid, redirect_uri, 'snsapi_userinfo')

        return url

    def get_uid(self, request, auth_code):
        " 获取授权token "

        if self.name == 'wechat':
            url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (self.appid, self.secret, auth_code)
        elif self.name == 'qq':
            redirect_uri = request.build_absolute_uri(request.path)
            url = 'https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&client_id=%s&client_secret=%s&code=%s&redirect_uri=%s' % (self.appid, self.secret, auth_code, redirect_uri)
            try:
                with urllib.request.urlopen(url) as f:
                    result = f.read().decode('utf8')
                    logger.warning(result)
                    result = urllib.parse.parse_qs(result)['access_token'][0]
            except Exception as e:
                logger.error(e)
                raise ValueError('Token请求失败')
            try:
                url = 'https://graph.qq.com/oauth2.0/me?access_token=%s' % result
                with urllib.request.urlopen(url) as f:
                    result = f.read().decode('utf8')
                    logger.warning(result)
                    #result = json.loads(result)

                return result.split('"')[7]
            except Exception as e:
                logger.error(e)
                raise ValueError('请求失败')

        elif self.name == 'douyin':
            url = 'https://developer.toutiao.com/api/apps/jscode2session?appid={0}&secret={1}&code={2}'.format(self.appid, self.secret, auth_code)

        elif self.name == 'wxb':
            url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(self.appid, self.secret, auth_code)
        elif self.name == 'wxa':
            url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(self.appid, self.secret, auth_code)

        logger.debug(url)

        with urllib.request.urlopen(url) as f:
            result = f.read().decode('utf8')
            result = json.loads(result)

        logger.warning(result)

        #return result['openid']

        return result


    class Meta:
        verbose_name = _('provider')
        verbose_name_plural = _('provider')


class Social(models.Model):
    """ 第三方登录 """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            verbose_name=_('user'))
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE,
            verbose_name=_('provider'))
    uid = models.CharField(_('uid'), max_length=200)
    nickname = models.CharField(_('nickname'), max_length=100,
            blank=True, null=True)
    avatar = models.URLField(_('avatar'), max_length=255,
            blank=True, null=True)
    extra_data = JSONField(_('extra date'), blank=True, null=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-created']
        unique_together = ['provider', 'uid']
        verbose_name = _('social')
        verbose_name_plural = _('social')
