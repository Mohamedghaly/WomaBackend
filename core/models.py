from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, help_text="HEX color code, e.g. #FFFFFF")

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=20)
    sort_order = models.IntegerField(default=0, help_text="Order to display sizes")

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

class DeliveryLocation(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.price})"
