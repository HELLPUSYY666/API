from django.core.validators import MaxLengthValidator
from rest_framework import serializers
from .models import User, Profile, Post, Group, Like, GroupMembership, Comment


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'groups', 'mobile', 'date_joined', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'first_name': {'validators': [MaxLengthValidator(240)]},
            'last_name': {'validators': [MaxLengthValidator(240)]},

        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({"password": "This field is required."})

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

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
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

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


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = ['user', 'post', 'created_at']


class GroupMembershipSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = GroupMembership
        fields = ['user', 'joined_at', 'post']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'
