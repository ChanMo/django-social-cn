from django.urls import path
from .views import *

urlpatterns = [
        path('auth/<str:provider>/', auth_view)
]
