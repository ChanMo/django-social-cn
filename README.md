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

2. 更新`urls.py`

```python
path('social/', include('social.urls')),
```

3. 执行`python manage.py migrate`
