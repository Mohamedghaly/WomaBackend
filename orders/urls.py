from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminOrderViewSet, CustomerOrderViewSet

router = DefaultRouter()

# Admin routes
router.register(r'admin/orders', AdminOrderViewSet, basename='admin-order')

# Customer routes
router.register(r'orders', CustomerOrderViewSet, basename='order')

urlpatterns = router.urls
