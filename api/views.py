from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework import generics


class UserAPIList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'post': UserSerializer(user).data})
        else:
            users = User.objects.all()
            return Response({'posts': UserSerializer(users, many=True).data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'error': 'Pk must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'error': 'Pk must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'message': f'User with id {pk} has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
