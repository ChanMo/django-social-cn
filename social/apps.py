from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SocialConfig(AppConfig):
    name = 'social'
    verbose_name = _('social')

    def ready(self):
        import social.receivers
