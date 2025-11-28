from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminCategoryViewSet, 
    AdminProductViewSet,
    AdminProductVariationViewSet,
    CategoryViewSet,
    ProductViewSet
)

router = DefaultRouter()

# Admin routes
router.register(r'admin/categories', AdminCategoryViewSet, basename='admin-category')
router.register(r'admin/products', AdminProductViewSet, basename='admin-product')
router.register(r'admin/variations', AdminProductVariationViewSet, basename='admin-variation')

# Public routes
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = router.urls
