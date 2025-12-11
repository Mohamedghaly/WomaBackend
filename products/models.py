import uuid
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Product category model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Product model representing items for sale.
    Stock is now calculated from variations if they exist.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0, help_text="Base stock (used only if no variations)")
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def in_stock(self):
        """
        Check if product is in stock.
        If has variations, check variation stock. Otherwise check base stock.
        """
        if self.variations.filter(is_active=True).exists():
            return self.variations.filter(is_active=True, stock_quantity__gt=0).exists()
        return self.stock_quantity > 0
    
    @property
    def total_stock(self):
        """
        Calculate total stock from all active variations.
        If no variations, return base stock.
        """
        active_variations = self.variations.filter(is_active=True)
        if active_variations.exists():
            from django.db.models import Sum
            total = active_variations.aggregate(total=Sum('stock_quantity'))['total']
            return total or 0
        return self.stock_quantity
    
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)




class ProductVariation(models.Model):
    """
    Product variations with dynamic attributes.
    Users can define any variation attributes (e.g., Color: Red, Memory: 256GB, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    # Custom name for the variation
    name = models.CharField(
        max_length=200,
        help_text="Variation name (e.g., 'Red Large Premium')"
    )
    
    # Dynamic attributes stored as JSON: {"attribute_name": "attribute_value"}
    # Example: {"Color": "Red", "Size": "Large", "Memory": "256GB"}
    attributes = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom variation attributes as key-value pairs"
    )
    
    # Variation-specific pricing and inventory
    price_adjustment = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text="Additional price for this variation (can be negative)"
    )
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_variations'
        ordering = ['name']
        indexes = [
            models.Index(fields=['product', 'is_active']),
            models.Index(fields=['sku']),
        ]
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
    @property
    def display_name(self):
        """Get the display name for this variation."""
        return self.name
    
    @property
    def attributes_display(self):
        """Get formatted attributes for display."""
        if not self.attributes:
            return "Standard"
        return " | ".join([f"{k}: {v}" for k, v in self.attributes.items()])
    
    @property
    def final_price(self):
        """Calculate final price including adjustment."""
        return self.product.price + self.price_adjustment
    
    @property
    def in_stock(self):
        """Check if variation is in stock."""
        return self.stock_quantity > 0
    
    def save(self, *args, **kwargs):
        """Auto-generate SKU if not provided."""
        if not self.sku:
            import random
            import string
            # Generate SKU from product ID and variation name + random suffix to ensure uniqueness
            base = str(self.product.id)[:8]
            name_part = self.name[:10].upper().replace(' ', '-')
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            self.sku = f"{base}-{name_part}-{random_suffix}"
            
        try:
            super().save(*args, **kwargs)
        except Exception:
            # If still collision (very rare), try one more time with new random suffix
            import random
            import string
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            self.sku = f"{base}-{name_part}-{random_suffix}"
            super().save(*args, **kwargs)



class VariationImage(models.Model):
    """
    Images for product variations.
    Each variation can have multiple images.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'variation_images'
        ordering = ['display_order', 'created_at']
        indexes = [
            models.Index(fields=['variation', 'is_primary']),
        ]
    
    def __str__(self):
        return f"Image for {self.variation}"
    
    def save(self, *args, **kwargs):
        """Ensure only one primary image per variation."""
        if self.is_primary:
            # Set other images of this variation to not primary
            VariationImage.objects.filter(
                variation=self.variation,
                is_primary=True
            ).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)
