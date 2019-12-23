from django.urls import path

from .views import *

urlpatterns = [
    path('update/', SocialUpdateView.as_view()),
    path('<slug:provider>/', AuthView.as_view()),
]
