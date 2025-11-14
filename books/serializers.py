from rest_framework import serializers
from .models import Author, Book, UserBook
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'isbn', 'publication_year', 'cover_image_url']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

class UserBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True) 

    class Meta:
        model = UserBook
        fields = ['id', 'book', 'status', 'rating', 'private_notes']

class UserBookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        fields = ['book', 'status']