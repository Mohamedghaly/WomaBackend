from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, OrderListSerializer


class AdminOrderViewSet(viewsets.ModelViewSet):
    """
    Admin viewset for managing all orders.
    Only accessible by admin users.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer


class CustomerOrderViewSet(viewsets.ModelViewSet):
    """
    Customer viewset for managing their own orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only current user's orders."""
        if self.request.user.is_authenticated:
            return Order.objects.filter(customer=self.request.user).select_related('customer').prefetch_related('items__product')
        return Order.objects.none()
    
    def get_permissions(self):
        """Allow anyone to create orders, but only authenticated users to list/retrieve."""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        """Use appropriate serializer based on action."""
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'list':
            return OrderListSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        """Set the customer if authenticated."""
        if self.request.user.is_authenticated:
            serializer.save(customer=self.request.user)
        else:
            serializer.save(customer=None)
            
    def create(self, request, *args, **kwargs):
        """Create order and return detailed response."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if request.user.is_authenticated:
            order = serializer.save(customer=request.user)
        else:
            order = serializer.save(customer=None)
        
        # Return full order details
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
