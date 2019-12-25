# Django Social APP

基于django的社交帐号APP

包含微信APP, 微信小程序, 微信公众号, 抖音小程序, QQ开放平台等


## Quick start

1. 更新`settings.py`

```python
INSTALLED_APPS = [
    ...
    'social',
]
```

2. 执行`python manage.py migrate`

## Web使用
用于微信web开放平台, 微信公众号, QQ开放平台

### AuthView

方式一, 直接使用
修改`urls.py`
```python
from social.views import AuthView

urlpatterns = [
    ...
    path('social/<slug:provider>/', AuthView.as_view()),
]
```

方式二, 继承
修改`views.py`

```python
from social.views import AuthView as BaseAuthView

class AuthView(BaseAuthView):
    success_url = '/success/'
```

## API使用
用于微信APP, 微信小程序, 抖音小程序

API使用[django-rest-framework](https://www.django-rest-framework.org/)框架, Token使用[django-rest-framework-simplejwt](https://github.com/davesque/django-rest-framework-simplejwt)

安装依赖

```bash
$ pip install djangorestfamework
$ pip install django-rest-famework-simplejwt

```

直接使用

```
from social.apis import AuthView, SocialUpdateView

urlpatterns = [
    ...
    path('social/auth/<slug:provider>/', AuthView.as_view()),
    path('social/update/', SocialUpdateView.as_view()),
]
```
