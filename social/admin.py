from django.contrib import admin

from .models import *


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'appid', 'url', 'created', 'updated')

class SocialAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'uid', 'created', 'updated')
    list_filter = ('provider', 'created', 'updated')
    list_per_page = 12
    search_fields = ('user__username', 'uid')


admin.site.register(Social, SocialAdmin)
admin.site.register(Provider, ProviderAdmin)
