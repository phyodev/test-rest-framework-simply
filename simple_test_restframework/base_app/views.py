from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, GroupSerializer, MovieSerializer, ResourceSerializer
from .paginators import CustomLimitOffsetPagination
from .models import Movie, Resource
from .utils import decode_id

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # pagination_class = CustomLimitOffsetPagination
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        encrypted_id = self.kwargs['pk']
        decrypted_id = decode_id(encrypted_id)  # Decrypt the ID
        if decrypted_id is None:
            from rest_framework.exceptions import NotFound
            raise NotFound("Invalid ID")
        return self.get_queryset().get(id=decrypted_id)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = CustomLimitOffsetPagination
    permission_classes = [
        permissions.IsAuthenticated
    ]

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = CustomLimitOffsetPagination

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    pagination_class = CustomLimitOffsetPagination