from rest_framework import serializers
from .models import Category, Product, ProductVariation, VariationImage


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'product_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')
    
    def get_product_count(self, obj):
        """Get count of active products in this category."""
        return obj.products.filter(is_active=True).count()


class VariationImageSerializer(serializers.ModelSerializer):
    """Serializer for VariationImage model."""
    
    class Meta:
        model = VariationImage
        fields = ('id', 'image_url', 'is_primary', 'display_order', 'created_at')
        read_only_fields = ('id', 'created_at')


from core.models import Color

class ProductVariationSerializer(serializers.ModelSerializer):
    """Serializer for ProductVariation model with dynamic attributes."""
    
    images = VariationImageSerializer(many=True, read_only=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    display_name = serializers.CharField(read_only=True)
    attributes_display = serializers.CharField(read_only=True)
    color_hex = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductVariation
        fields = (
            'id', 'sku', 'name', 'display_name', 'attributes', 'attributes_display',
            'price_adjustment', 'final_price', 'stock_quantity', 
            'in_stock', 'is_active', 'images', 'color_hex', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'sku', 'created_at', 'updated_at')

    def get_color_hex(self, obj):
        """Get hex code for the color attribute if it exists."""
        attributes = obj.attributes or {}
        # Check for 'Color' or 'color' key
        color_name = attributes.get('Color') or attributes.get('color')
        
        if color_name:
            try:
                color_obj = Color.objects.filter(name__iexact=color_name).first()
                if color_obj:
                    return color_obj.hex_code
            except Exception:
                pass
        return None
    
    def validate_stock_quantity(self, value):
        """Ensure stock quantity is not negative."""
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value


class ProductVariationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating product variations with dynamic attributes and images."""
    
    images = VariationImageSerializer(many=True, required=False)
    
    class Meta:
        model = ProductVariation
        fields = ('product', 'name', 'attributes', 'price_adjustment', 'stock_quantity', 'is_active', 'images')
    
    def validate_name(self, value):
        """Ensure name is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("Variation name is required.")
        return value
    
    def validate_stock_quantity(self, value):
        """Ensure stock quantity is not negative."""
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value
    
    def create(self, validated_data):
        """Create variation with images."""
        images_data = validated_data.pop('images', [])
        variation = ProductVariation.objects.create(**validated_data)
        
        # Create images
        for image_data in images_data:
            VariationImage.objects.create(variation=variation, **image_data)
        
        return variation

    def update(self, instance, validated_data):
        """Update variation and its images."""
        images_data = validated_data.pop('images', [])
        
        # Update standard fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update images if provided
        if images_data:
            # For simplicity, we'll remove existing images and add new ones
            # In a more complex app, we might want to update existing ones
            instance.images.all().delete()
            for image_data in images_data:
                VariationImage.objects.create(variation=instance, **image_data)
                
        return instance


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model with variations."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    variations = ProductVariationSerializer(many=True, read_only=True)
    variation_count = serializers.SerializerMethodField()
    total_stock = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'category', 'category_name', 'category_slug', 
            'name', 'slug', 'description', 'price', 
            'stock_quantity', 'total_stock', 'in_stock', 'image_url', 
            'is_active', 'variations', 'variation_count',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at', 'stock_quantity')
    
    def get_variation_count(self, obj):
        """Get count of active variations."""
        return obj.variations.filter(is_active=True).count()
    
    def validate_price(self, value):
        """Ensure price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product list view."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    has_variations = serializers.SerializerMethodField()
    variation_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = (
            'id', 'category_name', 'name', 'slug', 'price', 
            'in_stock', 'image_url', 'has_variations', 
            'variation_count', 'created_at'
        )
    
    def get_has_variations(self, obj):
        """Check if product has variations."""
        return obj.variations.filter(is_active=True).exists()
    
    def get_variation_count(self, obj):
        """Get count of active variations."""
        return obj.variations.filter(is_active=True).count()
