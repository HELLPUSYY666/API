from rest_framework import serializers
from .models import User, Profile, Post, Group


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'groups', 'mobile', 'date_joined']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


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
    members = UserSerializer(many=True, read_only=True)
    posts = PostSerializer(source='user.posts', many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
