from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import *


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'appid', 'created', 'updated')

class SocialAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'show_avatar', 'provider', 'uid', 'created', 'updated')
    list_filter = ('provider', 'created', 'updated')
    list_per_page = 12
    search_fields = ('user__username', 'uid', 'nickname')
    raw_id_fields = ('user',)

    def show_avatar(self, obj):
        if not obj.avatar:
            return None

        return format_html('<img src="{}" alt="{}" width="24" height="24" />', obj.avatar, obj.user.username)
    show_avatar.short_description = _('avatar')



admin.site.register(Social, SocialAdmin)
admin.site.register(Provider, ProviderAdmin)
