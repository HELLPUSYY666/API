from django.urls import path, include
from .views import *
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('users/', UserAPIList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserAPIDetail.as_view(), name='user-detail'),
    path('users_del/<int:pk>/', UserAPIDelete.as_view(), name='user-delete'),
]
