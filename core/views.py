from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Color, Size, DeliveryLocation
from .serializers import ColorSerializer, SizeSerializer, DeliveryLocationSerializer

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class DeliveryLocationViewSet(viewsets.ModelViewSet):
    queryset = DeliveryLocation.objects.all()
    serializer_class = DeliveryLocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum
from products.models import Product, Category
from orders.models import Order
from django.contrib.auth import get_user_model

class DashboardStatsView(APIView):
    """
    Return dashboard statistics.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status='pending').count()
        
        # Calculate total revenue from completed orders
        total_revenue = Order.objects.filter(status='completed').aggregate(
            total=Sum('total_amount')
        )['total'] or 0.00
        
        User = get_user_model()
        total_customers = User.objects.filter(is_staff=False).count()

        return Response({
            'total_products': total_products,
            'total_categories': total_categories,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'total_revenue': total_revenue,
            'total_customers': total_customers
        })

class WebsiteSettingsView(APIView):
    """
    Get or update website settings (singleton).
    GET: Public access to read settings
    PUT: Admin only to update settings
    """
    def get_permissions(self):
        if self.request.method == 'GET':
            return []  # Public access for GET
        return [IsAdminUser()]  # Admin only for PUT
    
    def get(self, request):
        from .models import WebsiteSettings
        from .serializers import WebsiteSettingsSerializer
        
        settings = WebsiteSettings.load()
        serializer = WebsiteSettingsSerializer(settings)
        return Response(serializer.data)
    
    def put(self, request):
        from .models import WebsiteSettings
        from .serializers import WebsiteSettingsSerializer
        
        settings = WebsiteSettings.load()
        serializer = WebsiteSettingsSerializer(settings, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
