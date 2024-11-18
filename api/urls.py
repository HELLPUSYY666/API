import djoser
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from djoser import urls
from .views import *

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/create/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='user-detail'),
    path('users/<int:pk>/delete/', UserViewSet.as_view({'delete': 'destroy'}), name='user-delete'),
    path('auth/', include(djoser.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('post/', PostViewSet.as_view({'post': 'create'}), name='post_create'),
    path('posts/', PostViewSet.as_view({'get': 'list'}), name='post'),
    path('post/<int:pk>/', PostViewSet.as_view({'put': 'update'}), name='post_up'),
    path('post/<int:pk>/delete/', PostViewSet.as_view({'delete': 'destroy'}), name='post_delete'),
    path('profile/', ProfileViewSet.as_view({'get': 'list'}), name='profile'),
    path('profile/create/', ProfileViewSet.as_view({'post': 'create'}), name='profile_create'),
    path('profile/<int:pk>/delete/', ProfileViewSet.as_view({'delete': 'destroy'}), name='profile_delete'),
    path('groups/', GroupViewSet.as_view({'get': 'list'}), name='groups'),
    path('groups/create/', GroupViewSet.as_view({'post': 'create'}), name='groups-create'),
    path('groups/<int:pk>/delete/', GroupViewSet.as_view({'delete': 'destroy'}), name='groups-delete'),
    path('groups/<int:pk>/join/', GroupViewSet.as_view({'post': 'join'}), name='groups-join'),
    path('groups/<int:pk>/leave/', GroupViewSet.as_view({'post': 'leave'}), name='groups-join'),

    # после join передать access токен
]
