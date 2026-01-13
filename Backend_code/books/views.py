from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author', 'category']

    def get_permissions(self):
        """Define permissions based on action"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Admin only for write operations
            permission_classes = [IsAdminUser]
        elif self.action == 'by_category':
            # Public access for by-category
            permission_classes = [AllowAny]
        elif hasattr(self, 'request') and self.request.path and 'by-category' in self.request.path:
            # Public access for by-category endpoint
            permission_classes = [AllowAny]
        else:
            # Authenticated users can read list/detail
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path='by-category', permission_classes=[AllowAny])
    def by_category(self, request):
        """Group books by category - public access"""
        books = self.get_queryset()
        categories = {}
        for book in books:
            cat = book.category or 'Uncategorized'
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'cover_image': book.cover_image.url if book.cover_image else None,
            })
        return Response(categories)

    @action(detail=False, methods=['get'], url_path='count', permission_classes=[IsAuthenticated])
    def count(self, request):
        """Get total book count"""
        count = self.get_queryset().count()
        return Response({'count': count})

