from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductVariation, VariationImage
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    ProductListSerializer,
    ProductVariationSerializer,
    ProductVariationCreateSerializer,
    VariationImageSerializer
)
from .permissions import IsAdminUser, IsAdminOrReadOnly


class AdminCategoryViewSet(viewsets.ModelViewSet):
    """
    Admin-only CRUD operations for categories.
    
    Endpoints:
    - GET    /api/v1/admin/categories/        - List all categories
    - POST   /api/v1/admin/categories/        - Create category
    - GET    /api/v1/admin/categories/{id}/   - Get category details
    - PUT    /api/v1/admin/categories/{id}/   - Update category
    - DELETE /api/v1/admin/categories/{id}/   - Delete category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'


class AdminProductViewSet(viewsets.ModelViewSet):
    """
    Admin-only CRUD operations for products.
    
    Endpoints:
    - GET    /api/v1/admin/products/        - List all products
    - POST   /api/v1/admin/products/        - Create product
    - GET    /api/v1/admin/products/{id}/   - Get product details
    - PUT    /api/v1/admin/products/{id}/   - Update product
    - DELETE /api/v1/admin/products/{id}/   - Delete product
    """
    queryset = Product.objects.select_related('category').prefetch_related('variations__images').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at', 'stock_quantity']
    ordering = ['-created_at']
    lookup_field = 'id'


class AdminProductVariationViewSet(viewsets.ModelViewSet):
    """
    Admin-only CRUD operations for product variations.
    
    Endpoints:
    - GET    /api/v1/admin/variations/           - List all variations
    - POST   /api/v1/admin/variations/           - Create variation
    - GET    /api/v1/admin/variations/{id}/      - Get variation details
    - PUT    /api/v1/admin/variations/{id}/      - Update variation
    - DELETE /api/v1/admin/variations/{id}/      - Delete variation
    """
    queryset = ProductVariation.objects.select_related('product').prefetch_related('images').all()
    serializer_class = ProductVariationSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'is_active']
    search_fields = ['sku', 'product__name', 'name']
    ordering_fields = ['final_price', 'stock_quantity', 'created_at']
    ordering = ['-created_at']
    lookup_field = 'id'
    
    def get_serializer_class(self):
        """Use create serializer for POST/PUT."""
        if self.action in ['create', 'update', 'partial_update']:
            return ProductVariationCreateSerializer
        return ProductVariationSerializer
    
    @action(detail=True, methods=['post'])
    def add_image(self, request, id=None):
        """Add an image to a variation."""
        variation = self.get_object()
        serializer = VariationImageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(variation=variation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public read-only operations for categories.
    
    Endpoints:
    - GET /api/v1/categories/      - List all categories
    - GET /api/v1/categories/{id}/ - Get category details
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public read-only operations for products.
    
    Endpoints:
    - GET /api/v1/products/           - List active products
    - GET /api/v1/products/{slug}/    - Get product details (with variations)
    
    Query parameters:
    - category: Filter by category slug
    - search: Search in name and description
    - ordering: Sort by name, price, created_at
    """
    queryset = Product.objects.select_related('category').prefetch_related(
        'variations__images'
    ).filter(is_active=True)
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view."""
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
