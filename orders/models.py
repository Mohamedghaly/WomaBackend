import uuid
from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    """
    Order model for customer purchases.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_address = models.TextField()
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Order {self.id} - {self.customer_email or 'Guest'}"
    
    def calculate_total(self):
        """Calculate and update total amount from order items."""
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])
        return total


class OrderItem(models.Model):
    """
    Individual items in an order.
    Supports ordering both simple products and product variations.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    variation = models.ForeignKey(
        'products.ProductVariation',
        related_name='order_items',
        on_delete=models.PROTECT,
        null=True,
        help_text="Specific product variation ordered (e.g., Red-Large)"
    )
    quantity = models.IntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'order_items'
    
    def __str__(self):
        if self.variation:
            return f"{self.quantity}x {self.variation}"
        return f"{self.quantity}x {self.product.name}"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this item."""
        return self.quantity * self.price_at_purchase
    
    def save(self, *args, **kwargs):
        """Auto-set price at purchase if not provided."""
        if not self.price_at_purchase:
            # Use variation price if available, otherwise product price
            if self.variation:
                self.price_at_purchase = self.variation.final_price
            else:
                self.price_at_purchase = self.product.price
        super().save(*args, **kwargs)
