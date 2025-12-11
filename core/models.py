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

class WebsiteSettings(models.Model):
    """
    Singleton model for website settings.
    Only one instance should exist.
    """
    # Branding
    site_name = models.CharField(max_length=100, default='WOMA Sportswear')
    site_tagline = models.CharField(max_length=200, default='Engineered for Performance')
    logo_url = models.URLField(max_length=500, blank=True)
    favicon_url = models.URLField(max_length=500, blank=True)
    
    # Hero/Banner
    hero_title = models.CharField(max_length=200, default='ELEVATE YOUR GAME')
    hero_subtitle = models.CharField(max_length=300, default='Premium sportswear designed for champions')
    hero_cta_text = models.CharField(max_length=50, default='Shop Now')
    hero_cta_link = models.CharField(max_length=200, default='/shop')
    hero_background_image = models.URLField(max_length=500, blank=True)
    
    # Theme Colors
    primary_color = models.CharField(max_length=7, default='#9333ea')  # Purple
    secondary_color = models.CharField(max_length=7, default='#db2777')  # Pink
    accent_color = models.CharField(max_length=7, default='#f472b6')  # Light pink
    background_color = models.CharField(max_length=7, default='#000000')  # Black
    text_color = models.CharField(max_length=7, default='#ffffff')  # White
    
    # About Section
    about_title = models.CharField(max_length=200, default='About WOMA Sportswear')
    about_description = models.TextField(default='Reimagining sportswear through a lens of modern utility and uncompromising performance.')
    about_image = models.URLField(max_length=500, blank=True)
    
    # Social Media
    instagram_url = models.URLField(max_length=500, blank=True)
    tiktok_url = models.URLField(max_length=500, blank=True)
    twitter_url = models.URLField(max_length=500, blank=True)
    youtube_url = models.URLField(max_length=500, blank=True)
    
    # Contact
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_address = models.TextField(blank=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Features
    show_newsletter = models.BooleanField(default=True)
    show_chat = models.BooleanField(default=False)
    maintenance_mode = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Website Settings'
        verbose_name_plural = 'Website Settings'
    
    def save(self, *args, **kwargs):
        """
        Ensure only one instance exists (Singleton pattern)
        """
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        """
        Load settings, create if doesn't exist
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return f"Website Settings - {self.site_name}"
