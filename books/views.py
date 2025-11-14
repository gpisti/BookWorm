from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from .models import UserBook
from .serializers import (
    RegisterSerializer, 
    UserBookSerializer, 
    UserBookCreateSerializer
)
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


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

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_book_by_isbn(request):
    isbn = request.query_params.get('isbn')
    
    if not isbn:
        return Response(
            {"error": "Az 'isbn' paraméter kötelező."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        book_data_key = f'ISBN:{isbn}'
        if book_data_key in data:
            return Response(data[book_data_key], status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "A könyv nem található ezzel az ISBN számmal."}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
    except requests.RequestException as e:
        return Response(
            {"error": f"Hiba a külső API hívása közben: {e}"}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )