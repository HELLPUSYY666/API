from rest_framework import serializers
from .models import User, Profile, Post, Group


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'groups', 'mobile', 'date_joined']

    def get_full_name(self, obj):
        first_name = obj.first_name or ''
        last_name = obj.last_name or ''
        return f"{first_name} {last_name}".strip()


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'avatar']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = '__all__'

    def get_posts(self, obj):
        posts = Post.objects.filter(user__in=obj.members.all())
        return PostSerializer(posts, many=True).data
