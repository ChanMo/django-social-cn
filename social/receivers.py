import logging
import urllib.request

from django.dispatch import receiver

from .models import *
from .signals import social_auth_done

logger = logging.getLogger(__name__)

@receiver(social_auth_done)
def update_user_info(sender, so, **kwargs):
    if so.provider.name == 'wxb':
        try:
            url = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN'.format(so.extra_data['access_token'], so.uid)
            logger.info(url)
            with urllib.request.urlopen(url) as f:
                result = f.read().decode('utf8')
                result = json.loads(result)
                logger.info(result)
                so.nickname = result['nickname']
                so.avatar = result['headimgurl']
                so.save()
        except Exception as e:
            logger.warning(e)
