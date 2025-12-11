# Custom Variation Names - Feature Guide

## Overview
Variations now support **custom editable names** instead of just auto-generated names from color/size/material!

---

## How It Works

### Option 1: Custom Name
Enter a custom name like:
- "Premium Edition"
- "Deluxe Pack"  
- "Limited Edition Gold"
- "Professional Bundle"

**Result:** Variation shows as `Premium Edition` everywhere

### Option 2: Auto-Generated (Default)
Leave name empty and fill color/size/material:
- Color: Red
- Size: Large  
- Material: Cotton

**Result:** Variation shows as `Red / Large / Cotton`

---

## Dashboard Usage

### Adding a Variation

**With Custom Name:**
```
Variation Name: Premium Edition
Color: (optional)
Size: (optional)
Material: (optional)
Price Adj: +5.00
Stock: 100
```
→ Shows as **"Premium Edition"** in table

**With Auto-Generated Name:**
```
Variation Name: (leave empty)
Color: Red
Size: Large
Material: Cotton
Price Adj: 0.00
Stock: 50
```
→ Shows as **"Red / Large / Cotton"** in table

**Minimal Auto-Generated:**
```
Variation Name: (leave empty)
Color: Blue
Size: (leave empty)
Material: (leave empty)
```
→ Shows as **"Blue"** in table

---

## Variations Table Display

The table now shows:

| Name | SKU | Color | Size | Material | Price Adj | Final Price | Stock | Actions |
|------|-----|-------|------|----------|-----------|-------------|-------|---------|
| **Premium Edition** | 1a2b3c4d-PREMIUM-E | - | - | - | +$5.00 | $34.99 | 100 | Delete |
| **Red / Large** | 1a2b3c4d-RED-LAR | Red | Large | - | +$2.00 | $31.99 | 50 | Delete |
| **Blue** | 1a2b3c4d-BLU | Blue | - | - | $0.00 | $29.99 | 30 | Delete |

---

## API Response

### With Custom Name:
```json
{
  "id": "...",
  "sku": "1a2b3c4d-PREMIUM-E",
  "name": "Premium Edition",
  "display_name": "Premium Edition",
  "color": null,
  "size": null,
  "material": null,
  "price_adjustment": "5.00",
  "final_price": "34.99",
  "stock_quantity": 100
}
```

### With Auto-Generated:
```json
{
  "id": "...",
  "sku": "1a2b3c4d-RED-LAR",
  "name": null,
  "display_name": "Red / Large",
  "color": "Red",
  "size": "Large",
  "material": null,
  "price_adjustment": "0.00",
  "final_price": "29.99",
  "stock_quantity": 50
}
```

---

## SKU Generation

### Custom Name:
`PRODUCT_ID-CUSTOM_NAME`
- "Premium Edition" → `1a2b3c4d-PREMIUM-ED`
- "Deluxe Pack" → `1a2b3c4d-DELUXE-PAC`

### Auto-Generated:
`PRODUCT_ID-COLOR-SIZE`
- Red/Large → `1a2b3c4d-RED-LAR`
- Blue/Small → `1a2b3c4d-BLU-SMA`

---

## Use Cases

### Fashion/Apparel:
Auto-generated works best:
- Red / Small
- Blue / Medium
- Black / Large / Cotton

### Special Editions:
Custom names work best:
- "Limited Edition Gold"
- "Founder's Pack"
- "Anniversary Bundle"
- "Professional Tier"

### Software/Digital:
Custom names:
- "Basic Plan"
- "Pro Plan"  
- "Enterprise Plan"

### Electronics:
Mix both:
- "Premium Edition" with color/size
- Or just "Space Gray / 256GB"

---

## Best Practices

✅ **Use custom names for:**
- Special editions
- Bundles/packages
- Subscription tiers
- Products where color/size don't apply

✅ **Use auto-generated for:**
- Standard color/size variations
- Physical products
- Apparel/fashion items

✅ **Combine both:**
- Name: "Premium Edition"
- Color: Gold
- Size: Large
→ Shows as "Premium Edition" but color data still available

---

## Migration Notes

- ✅ Existing variations: Will auto-generate from color/size/material
- ✅ New variations: Can use either custom or auto-generated
- ✅ Backward compatible: All existing code continues to work
- ✅ No data loss: Color/size/material still stored and displayed

---

## Database Changes

**New field:** `ProductVariation.name`
- Type: CharField(200)
- Optional: Can be null/blank
- Used for custom variation names

**New property:** `ProductVariation.display_name`
- Returns custom name if set
- Otherwise generates from color/size/material
- Always returns a readable name

---

**Status: ✅ Live and Ready to Use!**

Refresh your dashboard and start using custom variation names!
