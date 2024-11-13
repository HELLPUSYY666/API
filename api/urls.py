from django.urls import path
from .views import UserAPIView, UserAPIList

urlpatterns = [
    path('users/', UserAPIList.as_view(), name='users'),
    path('users/<int:pk>/', UserAPIList.as_view(), name='user'),
]