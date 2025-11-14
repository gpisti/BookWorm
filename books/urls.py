from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, UserBookViewSet, search_book_by_isbn

router = DefaultRouter()
router.register(r'my-books', UserBookViewSet, basename='my-books')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('external/search-isbn/', search_book_by_isbn, name='search_isbn'),
    
    path('', include(router.urls)),
]
