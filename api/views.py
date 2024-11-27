from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import User, Category, Post, Profile, Group, Like
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializer import UserSerializer, PostSerializer, ProfileSerializer, GroupSerializer, LikeSerializer, \
    GroupMembershipSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.exceptions import ValidationError, NotFound
from django.core.cache import cache


class UserAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = UserAPIListPagination
    # authentication_classes = [TokenAuthentication]


class PostAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_fields = ['created_at']

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

        cache_key = f"group_{group.id}_members"
        cached_members = cache.get(cache_key)

        if cached_members is not None:
            print("Кэш найден!")
            if user in cached_members:
                return Response({'message': 'Вы уже состоите в этой группе.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Кэш пуст!")
            if user in group.members.all():
                return Response({'message': 'Вы уже состоите в этой группе.'}, status=status.HTTP_400_BAD_REQUEST)

        group.members.add(user)
        cache.set(cache_key, group.members.all(), timeout=60 * 15)  # Кэшируем на 15 минут
        return Response({'message': 'Вы успешно вступили в группу!'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='leave')
    def leave(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        user = request.user

        # Проверка кэша
        cache_key = f"group_{group.id}_members"
        cached_members = cache.get(cache_key)

        if cached_members is not None:
            if user not in cached_members:
                return Response({'message': 'Вы не состоите в этой группе.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if user not in group.members.all():
                return Response({'message': 'Вы не состоите в этой группе.'}, status=status.HTTP_400_BAD_REQUEST)

        group.members.remove(user)
        cache.set(cache_key, group.members.all(), timeout=60 * 15)  # Кэшируем обновленный список на 15 минут
        return Response({'message': 'Вы успешно вышли из группы!'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        group = serializer.save()
        group.members.add(self.request.user)


class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        user = self.request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound("Post matching query does not exist.")

        if Like.objects.filter(user=user, post=post).exists():
            raise ValidationError("You have already liked this post.")

        serializer.save(user=user, post=post)

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.data['user'] = request.user.id
        else:
            raise ValidationError("Authentication required.")

        return super().create(request, *args, **kwargs)


class GroupMembersViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupMembershipSerializer


class PostLikesView(ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post_id=post_id)


class CommentView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        post_id = self.request.data.get('post_id')

        if not post_id:
            raise ValueError("Post ID is required to create a comment.")

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValueError("Post with the given ID does not exist.")

        serializer.save(user=user, post=post)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Comment added successfully!", "data": response.data},
            status=status.HTTP_201_CREATED
        )


def index(request):
    return render(request, 'api/index.html')
