from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    cat_id = serializers.IntegerField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)
