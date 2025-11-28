from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model."""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    variation_details = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'variation', 'variation_details', 
                  'quantity', 'price_at_purchase', 'subtotal')
        read_only_fields = ('id', 'price_at_purchase', 'subtotal')
    
    def get_variation_details(self, obj):
        """Get variation details if present."""
        if obj.variation:
            return {
                'id': str(obj.variation.id),
                'sku': obj.variation.sku,
                'color': obj.variation.color,
                'size': obj.variation.size,
                'material': obj.variation.material,
            }
        return None
    
    def validate_quantity(self, value):
        """Ensure quantity is positive."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating order items."""
    
    class Meta:
        model = OrderItem
        fields = ('product', 'variation', 'quantity')
    
    def validate_quantity(self, value):
        """Ensure quantity is positive."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
    
    def validate(self, data):
        """Validate variation belongs to product."""
        variation = data.get('variation')
        product = data.get('product')
        
        if variation and variation.product != product:
            raise serializers.ValidationError({
                "variation": "This variation does not belong to the selected product."
            })
        
        return data


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    
    items = OrderItemSerializer(many=True, read_only=True)
    customer_email = serializers.EmailField(source='customer.email', read_only=True)
    
    class Meta:
        model = Order
        fields = (
            'id', 'customer', 'customer_email', 'status', 
            'total_amount', 'shipping_address', 
            'items', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'customer', 'total_amount', 'created_at', 'updated_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders."""
    
    items = OrderItemCreateSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ('shipping_address', 'items')
    
    def validate_items(self, value):
        """Ensure items list is not empty."""
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value
    
    def validate(self, data):
        """Validate that products with variations must be ordered via variation."""
        items = data.get('items', [])
        
        for item_data in items:
            product = item_data.get('product')
            variation = item_data.get('variation')
            
            # Check if product has active variations
            if product and product.variations.filter(is_active=True).exists():
                if not variation:
                    raise serializers.ValidationError({
                        'items': f"Product '{product.name}' has variations. Please select a specific variation."
                    })
        
        return data
    
    def create(self, validated_data):
        """Create order with items."""
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        # Create order items
        for item_data in items_data:
            product = item_data['product']
            variation = item_data.get('variation')
            quantity = item_data['quantity']
            
            # For products with variations, variation is required
            if variation:
                # Check variation stock
                if variation.stock_quantity < quantity:
                    order.delete()
                    raise serializers.ValidationError({
                        'items': f"Insufficient stock for {variation}. Available: {variation.stock_quantity}"
                    })
                
                # Create order item with variation
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    variation=variation,
                    quantity=quantity,
                    price_at_purchase=variation.final_price
                )
                
                # Update variation stock
                variation.stock_quantity -= quantity
                variation.save(update_fields=['stock_quantity'])
            else:
                # Fallback for products without variations (legacy support)
                if product.stock_quantity < quantity:
                    order.delete()
                    raise serializers.ValidationError({
                        'items': f"Insufficient stock for {product.name}. Available: {product.stock_quantity}"
                    })
                
                # Create order item without variation
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price_at_purchase=product.price
                )
                
                # Update product stock
                product.stock_quantity -= quantity
                product.save(update_fields=['stock_quantity'])
        
        # Calculate order total
        order.calculate_total()
        
        return order


class OrderListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for order list view."""
    
    customer_email = serializers.EmailField(source='customer.email', read_only=True)
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ('id', 'customer_email', 'status', 'total_amount', 'item_count', 'created_at')
    
    def get_item_count(self, obj):
        """Get count of items in order."""
        return obj.items.count()
