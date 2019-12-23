from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import *

User = get_user_model()



class AuthViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('test')
        self.client.force_login(user)
        Provider.objects.create(name='wxb', appid='test', secret='test')

    def test(self):
        result = self.client.get('/social/wxb/')
        self.assertEqual(result.status_code, 302)

    def test(self):
        result = self.client.get('/social/wxb/?code=test')
        print(result)
        self.assertEqual(result.status_code, 400)
