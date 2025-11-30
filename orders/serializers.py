from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product, ProductVariation


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items."""
    product_name = serializers.CharField(source='product.name', read_only=True)
    variation_name = serializers.CharField(source='variation.__str__', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'variation', 'quantity', 'price_at_purchase', 'subtotal', 'product_name', 'variation_name')
        read_only_fields = ('price_at_purchase',)


class OrderCreateItemSerializer(serializers.Serializer):
    """Serializer for creating order items."""
    product_id = serializers.UUIDField()
    variation_id = serializers.UUIDField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders."""
    items = OrderCreateItemSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'shipping_address', 'items', 'total_amount', 'customer_name', 'customer_email')
        read_only_fields = ('total_amount', 'id')
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            variation = None
            if item_data.get('variation_id'):
                try:
                    variation = ProductVariation.objects.get(id=item_data['variation_id'])
                except ProductVariation.DoesNotExist:
                    pass
            
            quantity = item_data['quantity']
            
            # Check stock
            if variation:
                if variation.stock_quantity < quantity:
                    raise serializers.ValidationError(f"Not enough stock for {variation}")
            elif product.stock_quantity < quantity:
                raise serializers.ValidationError(f"Not enough stock for {product.name}")
            
            OrderItem.objects.create(
                order=order,
                product=product,
                variation=variation,
                quantity=quantity,
                price_at_purchase=item_data.get('price') or (variation.final_price if variation else product.price)
            )
            
            # Update stock
            if variation:
                variation.stock_quantity -= quantity
                variation.save()
            else:
                product.stock_quantity -= quantity
                product.save()
        
        order.calculate_total()
        return order


class OrderSerializer(serializers.ModelSerializer):
    """Detailed serializer for order view."""
    items = OrderItemSerializer(many=True, read_only=True)
    customer_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ('id', 'customer', 'customer_email', 'customer_name', 'status', 'total_amount', 'shipping_address', 'created_at', 'items')
        read_only_fields = ('customer', 'status', 'total_amount', 'created_at')

    def get_customer_email(self, obj):
        if obj.customer:
            return obj.customer.email
        return obj.customer_email


class OrderListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for order list view."""
    customer_email = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ('id', 'customer_email', 'customer_name', 'status', 'total_amount', 'item_count', 'created_at')
    
    def get_customer_email(self, obj):
        if obj.customer:
            return obj.customer.email
        return obj.customer_email
    
    def get_item_count(self, obj):
        return obj.items.count()
