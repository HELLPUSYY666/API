from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import User, Category
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser


class UserAPIList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]


class UserAPIDelete(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
