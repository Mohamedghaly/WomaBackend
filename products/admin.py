from django.contrib import admin
from .models import Category, Product, ProductVariation, VariationImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""
    
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')


class VariationImageInline(admin.TabularInline):
    """Inline admin for variation images."""
    model = VariationImage
    extra = 1
    fields = ('image_url', 'is_primary', 'display_order')


class ProductVariationInline(admin.TabularInline):
    """Inline admin for product variations."""
    model = ProductVariation
    extra = 1
    fields = ('name', 'sku', 'attributes', 'price_adjustment', 'stock_quantity', 'is_active')
    readonly_fields = ('sku',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""
    
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active', 'stock_quantity')
    inlines = [ProductVariationInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Media', {
            'fields': ('image_url',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    """Admin interface for ProductVariation model."""
    
    list_display = ('display_name', 'product', 'sku', 'attributes_display', 'final_price', 'stock_quantity', 'is_active')
    list_filter = ('product', 'is_active')
    search_fields = ('sku', 'product__name', 'name')
    readonly_fields = ('created_at', 'updated_at', 'display_name', 'attributes_display')
    inlines = [VariationImageInline]
    
    fieldsets = (
        ('Product', {
            'fields': ('product', 'sku')
        }),
        ('Variation Details', {
            'fields': ('name', 'attributes', 'display_name', 'attributes_display')
        }),
        ('Pricing & Inventory', {
            'fields': ('price_adjustment', 'stock_quantity', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VariationImage)
class VariationImageAdmin(admin.ModelAdmin):
    """Admin interface for VariationImage model."""
    
    list_display = ('variation', 'image_url', 'is_primary', 'display_order')
    list_filter = ('is_primary',)
    search_fields = ('variation__product__name',)
