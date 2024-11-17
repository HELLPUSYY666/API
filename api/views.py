from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import User, Category, Post, Profile, Group
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializer import UserSerializer, PostSerializer, ProfileSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.exceptions import ValidationError


class UserAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserAPIList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = UserAPIListPagination
    authentication_classes = [TokenAuthentication]  # Подключение аутентификации через токен


class UserAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]  # Подключение аутентификации через токен


class UserAPIDelete(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]


class PostAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if Profile.objects.filter(user=user).exists():
            raise ValidationError("A profile already exists for this user.")
        serializer.save(user=user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='join')
    def join(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        user = request.user

        if user in group.members.all():
            return Response({'message': 'Вы уже состоите в этой группе.'}, status=status.HTTP_400_BAD_REQUEST)

        group.members.add(user)
        return Response({'message': 'Вы успешно вступили в группу!'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='leave')
    def leave(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        user = request.user

        if user not in group.members.all():
            return Response({'message': 'Вы не состоите в этой группе.'}, status=status.HTTP_400_BAD_REQUEST)

        group.members.remove(user)
        return Response({'message': 'Вы успешно вышли из группы!'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        group = serializer.save()
        group.members.add(self.request.user)  # Добавляем создателя в группу
