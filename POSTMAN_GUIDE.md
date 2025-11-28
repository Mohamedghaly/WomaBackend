# Postman Collection Guide

## 📦 Import Files

Two files have been created for Postman:

1. **Collection**: `Woma_Ecommerce_API.postman_collection.json`
2. **Environment**: `Woma_Ecommerce_API.postman_environment.json`

## 🚀 Quick Setup

### Step 1: Import Collection
1. Open Postman
2. Click **Import** button (top left)
3. Select `Woma_Ecommerce_API.postman_collection.json`
4. Collection will appear in your sidebar

### Step 2: Import Environment
1. Click **Import** button again
2. Select `Woma_Ecommerce_API.postman_environment.json`
3. Select the environment from the dropdown (top right)

### Step 3: Start Backend Server
```bash
cd /Users/mohamedghaly/Desktop/WomaBackend
source venv/bin/activate
python manage.py runserver
```

## 📚 Collection Structure

The collection is organized into folders:

### 1️⃣ Authentication
- **Register User** - Create new account
- **Login** - Get JWT tokens (auto-saves to environment)
- **Refresh Token** - Refresh access token
- **Get Profile** - View user profile
- **Update Profile** - Update user info

### 2️⃣ Admin - Categories
- **List All Categories** - View all categories
- **Create Category** - Add new category (auto-saves ID)
- **Get Category by ID** - View category details
- **Update Category** - Edit category
- **Delete Category** - Remove category

### 3️⃣ Admin - Products
- **List All Products** - View all products
- **Filter Products by Category** - Filter by category
- **Search Products** - Search by name/description
- **Create Product** - Add new product (auto-saves ID)
- **Get Product by ID** - View product details
- **Update Product** - Edit product
- **Delete Product** - Remove product

### 4️⃣ Admin - Orders
- **List All Orders** - View all orders
- **Filter Orders by Status** - Filter by status
- **Get Order by ID** - View order details
- **Update Order Status** - Change order status

### 5️⃣ Public - Categories
- **List Categories** - Browse categories (no auth)
- **Get Category by Slug** - View by slug (no auth)

### 6️⃣ Public - Products
- **List Products** - Browse products (no auth)
- **Filter Products by Category** - Filter by category slug
- **Search Products** - Search products
- **Get Product by Slug** - View by slug (no auth)

### 7️⃣ Customer - Orders
- **List My Orders** - View own orders
- **Create Order** - Place new order (auto-saves ID)
- **Get Order by ID** - View order details
- **Filter My Orders by Status** - Filter own orders

## 🔑 Environment Variables

The environment includes these variables:

- `base_url` - API base URL (default: http://localhost:8000)
- `access_token` - JWT access token (auto-filled on login)
- `refresh_token` - JWT refresh token (auto-filled on login)
- `category_id` - Last created category ID (auto-filled)
- `category_slug` - Last created category slug (auto-filled)
- `product_id` - Last created product ID (auto-filled)
- `product_slug` - Last created product slug (auto-filled)
- `order_id` - Last created order ID (auto-filled)

## 🎯 Testing Workflow

### Complete Testing Flow:

1. **Login as Admin**
   - Run: `Authentication > Login`
   - Update credentials in request body
   - Tokens auto-saved ✅

2. **Create Category**
   - Run: `Admin - Categories > Create Category`
   - Category ID auto-saved ✅

3. **Create Product**
   - Run: `Admin - Products > Create Product`
   - Uses saved `category_id`
   - Product ID auto-saved ✅

4. **Browse Products (Public)**
   - Run: `Public - Products > List Products`
   - No authentication needed
   - Try filtering by category

5. **Register Customer**
   - Run: `Authentication > Register User`
   - Change role to "customer"
   - Login with customer credentials

6. **Create Order**
   - Run: `Customer - Orders > Create Order`
   - Uses saved `product_id`
   - Order ID auto-saved ✅

7. **Admin Views Order**
   - Login as admin again
   - Run: `Admin - Orders > List All Orders`
   - View customer's order

8. **Update Order Status**
   - Run: `Admin - Orders > Update Order Status`
   - Change status to "processing"

## 🔒 Authentication

Most endpoints require authentication:
- Collection uses Bearer Token authentication
- Token automatically used from `{{access_token}}`
- Login request auto-saves tokens
- Public endpoints have auth disabled

## 📝 Tips

### Auto-Save Features
Several requests have test scripts that auto-save IDs:
- Login → saves `access_token` and `refresh_token`
- Create Category → saves `category_id` and `category_slug`
- Create Product → saves `product_id` and `product_slug`
- Create Order → saves `order_id`

### Using Variables
Variables are referenced with double curly braces:
- `{{base_url}}`
- `{{access_token}}`
- `{{product_id}}`

### Filtering & Search
Query parameters are pre-configured:
- Status filters: `pending`, `processing`, `completed`, `cancelled`
- Search works on name and description
- Ordering: `name`, `price`, `created_at`, `-created_at`

### Before First Test
1. Make sure server is running
2. Create superuser if not done:
   ```bash
   python manage.py createsuperuser
   ```
3. Import both collection and environment
4. Select environment from dropdown

## 🐛 Troubleshooting

**401 Unauthorized**
- Run Login request first
- Check token is saved in environment
- Token may have expired (tokens last 1 hour)

**404 Not Found**
- Check server is running
- Verify `base_url` is correct
- Ensure entity IDs are saved

**400 Bad Request**
- Check request body format
- Verify required fields
- Check UUID format for IDs

**403 Forbidden**
- User doesn't have permission
- Admin endpoints require admin role
- Check user role in profile

## 📊 Sample Test Sequence

1. Login → Get token
2. Create Category → Electronics
3. Create Product → Headphones ($199.99)
4. View Public Products → See headphones
5. Register Customer → customer@test.com
6. Login as Customer → Get customer token
7. Create Order → Buy 2 headphones
8. View My Orders → See order
9. Login as Admin → Get admin token
10. View All Orders → See customer's order
11. Update Order Status → Set to "processing"

## 🎉 Ready to Test!

Your collection is ready to use. Start with the Login request and follow the testing workflow above.

Happy Testing! 🚀
