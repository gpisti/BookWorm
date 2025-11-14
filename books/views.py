from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from .models import UserBook, Book, Author
from .serializers import (
    RegisterSerializer, 
    UserBookSerializer
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
    serializer_class = UserBookSerializer

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
        if book_data_key not in data:
            return Response(
                {"error": "A könyv nem található ezzel az ISBN számmal."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        book_info = data[book_data_key]
        
        book, created = Book.objects.get_or_create(
            isbn=isbn,
            defaults={
                'title': book_info.get('title', 'Ismeretlen cím'),
                'publication_year': book_info.get('publish_date', '').split('-')[0] if book_info.get('publish_date') else None,
                'cover_image_url': book_info.get('cover', {}).get('large') or book_info.get('cover', {}).get('medium') or book_info.get('cover', {}).get('small') or None
            }
        )
        
        if book_info.get('authors'):
            for author_info in book_info['authors']:
                author_name = author_info.get('name', '')
                if author_name:
                    author, _ = Author.objects.get_or_create(name=author_name)
                    book.authors.add(author)
        
        from .serializers import BookSerializer
        serializer = BookSerializer(book)
        return Response({
            'book': serializer.data,
            'created': created
        }, status=status.HTTP_200_OK)
            
    except requests.RequestException as e:
        return Response(
            {"error": f"Hiba a külső API hívása közben: {e}"}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )