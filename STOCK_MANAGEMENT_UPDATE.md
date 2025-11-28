# Stock Management Update - Complete Summary

## Overview
The system has been updated to use **variation-based stock management** instead of manual product stock entry.

---

## Backend Changes

### 1. Product Model (`products/models.py`)
**Updated Properties:**
- `total_stock` - Calculates sum of all variation stocks, or base stock if no variations
- `in_stock` - Checks if any variation has stock > 0, or base stock if no variations
- `stock_quantity` - Now defaults to 0 and is read-only (used only for products without variations)

**How it works:**
```python
# Product with variations:
product.total_stock  # Returns sum of all variation stocks
product.in_stock     # Returns True if any variation has stock

# Product without variations (legacy):
product.total_stock  # Returns base stock_quantity
product.in_stock     # Returns stock_quantity > 0
```

### 2. Product Serializer (`products/serializers.py`)
**New Fields:**
- `total_stock` (read-only) - Shows calculated total from variations
- `stock_quantity` (read-only) - Base stock, not editable via API

**API Response:**
```json
{
  "id": "...",
  "name": "T-Shirt",
  "price": "29.99",
  "stock_quantity": 0,
  "total_stock": 45,  // NEW: Sum of variations
  "variation_count": 3,
  "variations": [...]
}
```

### 3. Order Creation (`orders/serializers.py`)
**Validation Added:**
- Products with variations **must** be ordered through a variation
- Trying to order a product directly when it has variations will return error:
  ```
  "Product 'T-Shirt' has variations. Please select a specific variation."
  ```

**Stock Deduction:**
- Orders with variations: Deducts from `variation.stock_quantity`
- Orders without variations: Deducts from `product.stock_quantity` (legacy support)

---

## Frontend Changes

### 1. Product Form (`dashboard/products.html`)
**Removed:**
- "Stock Quantity" field

**Added:**
- Hint: "Stock will be managed through variations"

**What admins enter:**
- Product Name
- Category
- Base Price (variations can adjust this)
- Description
- Image
- Active status

### 2. Products Table (`dashboard/js/products.js`)
**Column Changes:**
- "Stock" → "Total Stock"
- Shows sum of all variation stocks
- Updates automatically when variations change

**Display:**
```
Product           | Base Price | Total Stock | Variations
Premium T-Shirt   | $29.99     | 45          | 3 [Manage]
```

---

## User Workflow

### Create a Product
1. Click "Add Product"
2. Fill: Name, Category, Base Price ($29.99)
3. No stock field - it's automatic!
4. Save

### Add Variations
1. Click "Manage" or "Add" button
2. Click "➕ Add Variation"
3. Fill:
   - Color: Red
   - Size: Large
   - Price Adj: +$2.00
   - Stock: 20
4. Repeat for more variations

### Stock Calculation
```
Variations:
- Red Small:  10 units  ($29.99)
- Red Large:  20 units  ($31.99)
- Blue Medium: 15 units  ($29.99)
----------------------------
Total Stock:  45 units
```

### Customer Orders
**Valid Order:**
```json
{
  "items": [
    {
      "product": "product-uuid",
      "variation": "red-large-uuid",  // Required if product has variations
      "quantity": 2
    }
  ]
}
```

**Invalid Order (will fail):**
```json
{
  "items": [
    {
      "product": "product-uuid",
      "variation": null,  // ❌ Error if product has variations
      "quantity": 2
    }
  ]
}
```

---

## Key Benefits

✅ **Accurate Inventory** - Stock tracked per variation, not just per product  
✅ **No Manual Entry** - Stock calculated automatically  
✅ **Prevents Errors** - Can't order product without selecting variation  
✅ **Real-time Updates** - Total stock updates when variations change  
✅ **Legacy Support** - Products without variations still work  

---

## Migration Guide

### For Existing Products:
1. Products will show `total_stock: 0` until variations are added
2. Base `stock_quantity` remains as fallback
3. Add variations to start tracking stock properly

### For New Products:
1. Create product (stock will be 0)
2. Add variations with stock quantities
3. Total stock calculated automatically

---

## API Examples

### Get Product with Stock Info
```bash
GET /api/v1/products/premium-cotton-t-shirt/

Response:
{
  "name": "Premium Cotton T-Shirt",
  "price": "29.99",
  "stock_quantity": 0,
  "total_stock": 45,
  "in_stock": true,
  "variation_count": 3,
  "variations": [
    {
      "sku": "1a1b21c2-RED-LAR",
      "color": "Red",
      "size": "Large",
      "final_price": "31.99",
      "stock_quantity": 20,
      "in_stock": true
    },
    ...
  ]
}
```

### Create Order with Variation
```bash
POST /api/v1/orders/

{
  "shipping_address": "123 Main St",
  "items": [
    {
      "product": "product-uuid",
      "variation": "variation-uuid",  // Selects Red-Large
      "quantity": 2
    }
  ]
}
```

After order:
- Variation stock: 20 → 18
- Product total_stock: 45 → 43

---

## Testing

### Test Stock Calculation
1. Open dashboard
2. View products → see "Total Stock" column
3. Click "Manage" on a product
4. Add variation with stock: 10
5. Close modal → total stock shows 10
6. Add another variation with stock: 15
7. Total stock updates to 25 ✅

### Test Order Validation
1. Try to order product without variation (has variations)
2. Should get error ❌
3. Order with variation specified
4. Should succeed and reduce stock ✅

---

## Database Schema

No migration needed! Uses existing fields:
- `product.stock_quantity` - Kept for backward compatibility
- `variation.stock_quantity` - Per-variation stock
- `total_stock` - Calculated property (not stored)

---

**Status: ✅ Complete and Ready**

All backend functions updated, dashboard UI updated, and validation in place!
