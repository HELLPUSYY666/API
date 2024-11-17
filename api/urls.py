from django.urls import path, include, re_path
from .views import *
from rest_framework import routers
import djoser
from djoser import urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('users/', UserAPIList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserAPIDetail.as_view(), name='user-detail'),
    path('users_del/<int:pk>/', UserAPIDelete.as_view(), name='user-delete'),
    path('auth/', include(djoser.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('post/', PostViewSet.as_view({'post': 'create'}), name='post_create'),
    path('posts/', PostViewSet.as_view({'get': 'list'}), name='post'),
    path('post/<int:pk>', PostViewSet.as_view({'get': 'list', 'put': 'update'}), name='post_up'),
    path('post_del/<int:pk>', PostViewSet.as_view({'get': 'list', 'delete': 'destroy'}), name='post_delete'),

]
