# Product Variations Guide

## Overview

The Woma E-commerce API now supports **product variations** (like Shopify's variants system), allowing you to create products with multiple options such as:
- Color variations
- Size variations  
- Material variations
- Any custom attributes

Each variation can have:
- Unique SKU (auto-generated)
- Individual pricing (price adjustment)
- Separate stock quantities
- Multiple images per variation
- Active/inactive status

## Database Structure

### ProductVariation Model
- **product**: Foreign key to Product
- **sku**: Unique identifier (auto-generated)
- **color**: Color option (optional)
- **size**: Size option (optional)
- **material**: Material option (optional)
- **price_adjustment**: Added to base product price (can be negative)
- **stock_quantity**: Individual stock for this variation
- **is_active**: Active status

### VariationImage Model
- **variation**: Foreign key to ProductVariation
- **image_url**: Image URL
- **is_primary**: Primary image flag (one per variation)
- **display_order**: Display order for multiple images

## API Endpoints

### Admin - Variations

#### List All Variations
```
GET /api/v1/admin/variations/
Authorization: Bearer {admin_token}
```

**Query Parameters:**
- `product={uuid}` - Filter by product
- `color={value}` - Filter by color
- `size={value}` - Filter by size
- `is_active={true/false}` - Filter by status
- `search={query}` - Search in SKU, product name, color, size

#### Create Variation
```
POST /api/v1/admin/variations/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "product": "product-uuid",
  "color": "Red",
  "size": "Large",
  "material": null,
  "price_adjustment": "2.00",
  "stock_quantity": 50,
  "is_active": true,
  "images": [
    {
      "image_url": "https://example.com/tshirt-red-front.jpg",
      "is_primary": true,
      "display_order": 0
    },
    {
      "image_url": "https://example.com/tshirt-red-back.jpg",
      "is_primary": false,
      "display_order": 1
    }
  ]
}
```

**Response:**
```json
{
  "id": "variation-uuid",
  "sku": "1a1b21c2-RED-LAR",
  "color": "Red",
  "size": "Large",
  "material": null,
  "price_adjustment": "2.00",
  "final_price": "31.99",
  "stock_quantity": 50,
  "in_stock": true,
  "is_active": true,
  "images": [
    {
      "id": "image-uuid",
      "image_url": "https://example.com/tshirt-red-front.jpg",
      "is_primary": true,
      "display_order": 0
    },
    {
      "id": "image-uuid-2",
      "image_url": "https://example.com/tshirt-red-back.jpg",
      "is_primary": false,
      "display_order": 1
    }
  ],
  "created_at": "2025-11-28T19:00:00Z",
  "updated_at": "2025-11-28T19:00:00Z"
}
```

#### Add Image to Variation
```
POST /api/v1/admin/variations/{variation_id}/add_image/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "image_url": "https://example.com/tshirt-red-side.jpg",
  "is_primary": false,
  "display_order": 2
}
```

### Public - Products with Variations

#### Get Product Details (includes variations)
```
GET /api/v1/products/{product_slug}/
```

**Response:**
```json
{
  "id": "product-uuid",
  "category": "category-uuid",
  "category_name": "Clothing",
  "category_slug": "clothing",
  "name": "Premium Cotton T-Shirt",
  "slug": "premium-cotton-t-shirt",
  "description": "High-quality 100% cotton t-shirt",
  "price": "29.99",
  "stock_quantity": 100,
  "in_stock": true,
  "image_url": "https://example.com/tshirt-main.jpg",
  "is_active": true,
  "variation_count": 9,
  "variations": [
    {
      "id": "variation-uuid",
      "sku": "1a1b21c2-RED-MED",
      "color": "Red",
      "size": "Medium",
      "material": null,
      "price_adjustment": "0.00",
      "final_price": "29.99",
      "stock_quantity": 20,
      "in_stock": true,
      "is_active": true,
      "images": [
        {
          "id": "image-uuid",
          "image_url": "https://example.com/tshirt-red-front.jpg",
          "is_primary": true,
          "display_order": 0
        },
        {
          "id": "image-uuid-2",
          "image_url": "https://example.com/tshirt-red-back.jpg",
          "is_primary": false,
          "display_order": 1
        }
      ]
    }
    // ... more variations
  ],
  "created_at": "2025-11-28T19:00:00Z",
  "updated_at": "2025-11-28T19:00:00Z"
}
```

#### List Products with Variation Info
```
GET /api/v1/products/
```

**Response:**
```json
{
  "count": 1,
  "results": [
    {
      "id": "product-uuid",
      "category_name": "Clothing",
      "name": "Premium Cotton T-Shirt",
      "slug": "premium-cotton-t-shirt",
      "price": "29.99",
      "in_stock": true,
      "image_url": "https://example.com/tshirt-main.jpg",
      "has_variations": true,
      "variation_count": 9,
      "created_at": "2025-11-28T19:00:00Z"
    }
  ]
}
```

### Customer - Orders with Variations

#### Create Order with Variation
```
POST /api/v1/orders/
Authorization: Bearer {customer_token}
Content-Type: application/json

{
  "shipping_address": "123 Main St, New York, NY 10001",
  "items": [
    {
      "product": "product-uuid",
      "variation": "variation-uuid",  // Optional: specify variation
      "quantity": 2
    },
    {
      "product": "another-product-uuid",
      "variation": null,  // No variation, use base product
      "quantity": 1
    }
  ]
}
```

**Response:**
```json
{
  "id": "order-uuid",
  "customer": "customer-uuid",
  "customer_email": "customer@example.com",
  "status": "pending",
  "total_amount": "89.97",
  "shipping_address": "123 Main St, New York, NY 10001",
  "items": [
    {
      "id": "item-uuid",
      "product": "product-uuid",
      "product_name": "Premium Cotton T-Shirt",
      "variation": "variation-uuid",
      "variation_details": {
        "id": "variation-uuid",
        "sku": "1a1b21c2-RED-MED",
        "color": "Red",
        "size": "Medium",
        "material": null
      },
      "quantity": 2,
      "price_at_purchase": "29.99",
      "subtotal": "59.98"
    },
    {
      "id": "item-uuid-2",
      "product": "another-product-uuid",
      "product_name": "Another Product",
      "variation": null,
      "variation_details": null,
      "quantity": 1,
      "price_at_purchase": "29.99",
      "subtotal": "29.99"
    }
  ],
  "created_at": "2025-11-28T19:00:00Z",
  "updated_at": "2025-11-28T19:00:00Z"
}
```

## Example Workflows

### 1. Create Product with Variations

**Step 1**: Create the base product
```
POST /api/v1/admin/products/
{
  "category": "category-uuid",
  "name": "Premium Cotton T-Shirt",
  "description": "High-quality 100% cotton t-shirt",
  "price": "29.99",
  "stock_quantity": 100
}
```

**Step 2**: Create variations (repeat for each variation)
```
POST /api/v1/admin/variations/
{
  "product": "product-uuid",
  "color": "Red",
  "size": "Medium",
  "price_adjustment": "0.00",
  "stock_quantity": 20,
  "images": [...]
}
```

### 2. Customer Browses and Orders

**Step 1**: List products
```
GET /api/v1/products/
// Shows products with has_variations: true
```

**Step 2**: Get product details with variations
```
GET /api/v1/products/premium-cotton-t-shirt/
// See all available colors, sizes, prices, stock
```

**Step 3**: Create order with specific variation
```
POST /api/v1/orders/
{
  "items": [
    {
      "product": "product-uuid",
      "variation": "red-medium-variation-uuid",
      "quantity": 2
    }
  ]
}
```

## Sample Data

You can create sample data using the provided script:
```bash
python create_sample_variations.py
```

This creates:
- 1 Category (Clothing)
- 1 Product (Premium Cotton T-Shirt)
- 9 Variations (3 colors × 3 sizes)
- 18 Images (2 per variation)

## Key Features

✅ **Flexible Attributes**: Color, size, material (or any combination)
✅ **Individual Pricing**: Each variation can have price adjustment
✅ **Separate Stock**: Track inventory per variation
✅ **Multiple Images**: Each variation can have multiple images
✅ **Auto SKU**: Automatically generated unique SKUs
✅ **Validation**: Ensures variation belongs to product
✅ **Stock Management**: Automatic inventory reduction on orders
✅ **Price Locking**: Prices locked at purchase time

## Testing in Postman

Update your Postman collection imports to include the new variation endpoints, or manually add:

1. **List Variations**: `GET /api/v1/admin/variations/`
2. **Create Variation**: `POST /api/v1/admin/variations/`
3. **Update Variation**: `PUT /api/v1/admin/variations/{id}/`
4. **Delete Variation**: `DELETE /api/v1/admin/variations/{id}/`
5. **Add Image**: `POST /api/v1/admin/variations/{id}/add_image/`

For orders, update the create order request to include `variation` field in items.
