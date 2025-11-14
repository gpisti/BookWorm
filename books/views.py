from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from .models import UserBook
from .serializers import (
    RegisterSerializer, 
    UserBookSerializer, 
    UserBookCreateSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,) 
    serializer_class = RegisterSerializer


class UserBookViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return UserBookCreateSerializer
        return UserBookSerializer

    def get_queryset(self):
        return UserBook.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)