from django.dispatch import Signal

# 授权完成
social_auth_done = Signal(providing_args=['so'])
