#!/usr/bin/env python
"""
Script to create sample product variations for testing.
Run: python create_sample_variations.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from products.models import Category, Product, ProductVariation, VariationImage

def create_sample_data():
    """Create sample products with variations."""
    
    print("🛍️  Creating sample e-commerce data...\n")
    
    # Create category
    clothing_cat, created = Category.objects.get_or_create(
        name="Clothing",
        defaults={'description': "Men's and Women's Clothing"}
    )
    print(f"{'✅ Created' if created else '📌 Found'} category: {clothing_cat.name}")
    
    # Create product
    tshirt, created = Product.objects.get_or_create(
        name="Premium Cotton T-Shirt",
        defaults={
            'category': clothing_cat,
            'description': "High-quality 100% cotton t-shirt with comfortable fit",
            'price': 29.99,
            'stock_quantity': 100,
            'image_url': "https://example.com/tshirt-main.jpg",
            'is_active': True
        }
    )
    print(f"{'✅ Created' if created else '📌 Found'} product: {tshirt.name}\n")
    
    # Define variations
    variations_data = [
        {
            'color': 'Red',
            'size': 'Small',
            'price_adjustment': 0,
            'stock': 15,
            'images': [
                'https://example.com/tshirt-red-front.jpg',
                'https://example.com/tshirt-red-back.jpg'
            ]
        },
        {
            'color': 'Red',
            'size': 'Medium',
            'price_adjustment': 0,
            'stock': 20,
            'images': [
                'https://example.com/tshirt-red-front.jpg',
                'https://example.com/tshirt-red-back.jpg'
            ]
        },
        {
            'color': 'Red',
            'size': 'Large',
            'price_adjustment': 2.00,
            'stock': 18,
            'images': [
                'https://example.com/tshirt-red-front.jpg',
                'https://example.com/tshirt-red-back.jpg'
            ]
        },
        {
            'color': 'Blue',
            'size': 'Small',
            'price_adjustment': 0,
            'stock': 12,
            'images': [
                'https://example.com/tshirt-blue-front.jpg',
                'https://example.com/tshirt-blue-back.jpg'
            ]
        },
        {
            'color': 'Blue',
            'size': 'Medium',
            'price_adjustment': 0,
            'stock': 25,
            'images': [
                'https://example.com/tshirt-blue-front.jpg',
                'https://example.com/tshirt-blue-back.jpg'
            ]
        },
        {
            'color': 'Blue',
            'size': 'Large',
            'price_adjustment': 2.00,
            'stock': 22,
            'images': [
                'https://example.com/tshirt-blue-front.jpg',
                'https://example.com/tshirt-blue-back.jpg'
            ]
        },
        {
            'color': 'Black',
            'size': 'Small',
            'price_adjustment': 0,
            'stock': 10,
            'images': [
                'https://example.com/tshirt-black-front.jpg',
                'https://example.com/tshirt-black-back.jpg'
            ]
        },
        {
            'color': 'Black',
            'size': 'Medium',
            'price_adjustment': 0,
            'stock': 30,
            'images': [
                'https://example.com/tshirt-black-front.jpg',
                'https://example.com/tshirt-black-back.jpg'
            ]
        },
        {
            'color': 'Black',
            'size': 'Large',
            'price_adjustment': 2.00,
            'stock': 28,
            'images': [
                'https://example.com/tshirt-black-front.jpg',
                'https://example.com/tshirt-black-back.jpg'
            ]
        },
    ]
    
    print("Creating product variations...")
    for var_data in variations_data:
        variation, created = ProductVariation.objects.get_or_create(
            product=tshirt,
            color=var_data['color'],
            size=var_data['size'],
            defaults={
                'price_adjustment': var_data['price_adjustment'],
                'stock_quantity': var_data['stock'],
                'is_active': True
            }
        )
        
        if created:
            # Add images
            for idx, image_url in enumerate(var_data['images']):
                VariationImage.objects.create(
                    variation=variation,
                    image_url=image_url,
                    is_primary=(idx == 0),
                    display_order=idx
                )
            print(f"  ✅ Created: {variation.color} - {variation.size} (SKU: {variation.sku}) | Stock: {variation.stock_quantity} | Price: ${variation.final_price}")
        else:
            print(f"  📌 Exists: {variation.color} - {variation.size}")
    
    print(f"\n🎉 Sample data created successfully!")
    print(f"\n📊 Summary:")
    print(f"  - Category: {clothing_cat.name}")
    print(f"  - Product: {tshirt.name} (Base price: ${tshirt.price})")
    print(f"  - Variations: {ProductVariation.objects.filter(product=tshirt).count()}")
    print(f"  - Total images: {VariationImage.objects.filter(variation__product=tshirt).count()}")
    
    # Print example variation details
    example_var = ProductVariation.objects.filter(product=tshirt, color='Red', size='Medium').first()
    if example_var:
        print(f"\n📝 Example Variation:")
        print(f"  ID: {example_var.id}")
        print(f"  SKU: {example_var.sku}")
        print(f"  Color: {example_var.color}")
        print(f"  Size: {example_var.size}")
        print(f"  Final Price: ${example_var.final_price}")
        print(f"  In Stock: {example_var.stock_quantity} units")
        print(f"  Images: {example_var.images.count()}")

if __name__ == "__main__":
    create_sample_data()
