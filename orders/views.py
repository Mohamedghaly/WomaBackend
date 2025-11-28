from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Order
from .serializers import (
    OrderSerializer, 
    OrderCreateSerializer, 
    OrderListSerializer
)
from .permissions import IsOrderOwnerOrAdmin
from products.permissions import IsAdminUser


class AdminOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admin-only operations for viewing and managing orders.
    
    Endpoints:
    - GET    /api/v1/admin/orders/        - List all orders
    - GET    /api/v1/admin/orders/{id}/   - Get order details
    - PATCH  /api/v1/admin/orders/{id}/   - Update order status
    """
    queryset = Order.objects.select_related('customer').prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'customer']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    lookup_field = 'id'
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view."""
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer
    
    def partial_update(self, request, *args, **kwargs):
        """Allow admin to update order status."""
        instance = self.get_object()
        
        # Only allow status updates
        if 'status' not in request.data:
            return Response({
                'error': 'Only status can be updated'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({
                'error': 'Invalid status value'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        instance.status = new_status
        instance.save(update_fields=['status'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CustomerOrderViewSet(viewsets.ModelViewSet):
    """
    Customer operations for orders.
    
    Endpoints:
    - GET  /api/v1/orders/      - List customer's orders
    - POST /api/v1/orders/      - Create new order
    - GET  /api/v1/orders/{id}/ - Get order details
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrderOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    lookup_field = 'id'
    
    def get_queryset(self):
        """Return only orders for the current user (unless admin)."""
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'admin':
            return Order.objects.select_related('customer').prefetch_related('items__product').all()
        return Order.objects.filter(customer=user).select_related('customer').prefetch_related('items__product')
    
    def get_serializer_class(self):
        """Use appropriate serializer based on action."""
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'list':
            return OrderListSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        """Set the customer to the current user."""
        serializer.save(customer=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Create order and return detailed response."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(customer=request.user)
        
        # Return full order details
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
