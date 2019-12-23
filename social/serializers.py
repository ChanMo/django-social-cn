from rest_framework import serializers

from .models import *


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ('nickname', 'avatar', 'extra_data', 'updated')
