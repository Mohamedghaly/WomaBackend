# Woma E-commerce Backend API

A comprehensive Django REST Framework backend for an e-commerce platform, similar to Shopify's API design. This backend provides complete functionality for managing products, categories, orders, and user authentication with role-based access control.

## Features

### Admin Capabilities
- ✅ **Authentication**: Secure JWT-based admin login
- ✅ **Order Management**: View and manage all customer orders
- ✅ **Product Management**: Full CRUD operations for products
- ✅ **Category Management**: Full CRUD operations for categories
- ✅ **Dashboard Access**: Django admin interface for data management

### Customer Capabilities
- ✅ **User Registration & Login**: Secure JWT authentication
- ✅ **Product Browsing**: View products filtered by category
- ✅ **Product Search**: Search products by name and description
- ✅ **Order Creation**: Create orders with multiple items
- ✅ **Order History**: View personal order history
- ✅ **Stock Management**: Automatic inventory updates on order creation

## Technology Stack

- **Framework**: Django 5.0 + Django REST Framework 3.14
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: OpenAPI/Swagger (drf-spectacular)
- **CORS Support**: django-cors-headers

## Project Structure

```
WomaBackend/
├── ecommerce_project/     # Main project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
├── accounts/              # User authentication app
│   ├── models.py          # Custom User model
│   ├── serializers.py     # User serializers
│   ├── views.py           # Auth endpoints
│   └── urls.py            # Auth routes
├── products/              # Products & Categories app
│   ├── models.py          # Category & Product models
│   ├── serializers.py     # Product serializers
│   ├── views.py           # Product endpoints
│   ├── permissions.py     # Custom permissions
│   └── urls.py            # Product routes
├── orders/                # Orders app
│   ├── models.py          # Order & OrderItem models
│   ├── serializers.py     # Order serializers
│   ├── views.py           # Order endpoints
│   ├── permissions.py     # Order permissions
│   └── urls.py            # Order routes
├── requirements.txt       # Python dependencies
├── manage.py              # Django management script
└── .env.example           # Environment variables template
```

## Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- pip

### 1. Clone or Navigate to Project
```bash
cd /Users/mohamedghaly/Desktop/WomaBackend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
Create a PostgreSQL database:
```bash
createdb woma_ecommerce
```

### 5. Set Environment Variables
Copy `.env.example` to `.env` and update with your settings:
```bash
cp .env.example .env
```

Edit `.env`:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=woma_ecommerce
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

Follow prompts to create an admin account.

### 8. Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000`

## API Documentation

### Interactive API Docs
- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

### Django Admin
- **Admin Interface**: `http://localhost:8000/admin/`

## API Endpoints

### Authentication (`/api/v1/auth/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register/` | Register new user | No |
| POST | `/api/v1/auth/login/` | User login | No |
| POST | `/api/v1/auth/refresh/` | Refresh JWT token | No |
| GET | `/api/v1/auth/profile/` | Get user profile | Yes |
| PUT | `/api/v1/auth/profile/` | Update profile | Yes |

### Admin - Categories (`/api/v1/admin/categories/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/admin/categories/` | List all categories | Admin |
| POST | `/api/v1/admin/categories/` | Create category | Admin |
| GET | `/api/v1/admin/categories/{id}/` | Get category | Admin |
| PUT | `/api/v1/admin/categories/{id}/` | Update category | Admin |
| DELETE | `/api/v1/admin/categories/{id}/` | Delete category | Admin |

### Admin - Products (`/api/v1/admin/products/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/admin/products/` | List all products | Admin |
| POST | `/api/v1/admin/products/` | Create product | Admin |
| GET | `/api/v1/admin/products/{id}/` | Get product | Admin |
| PUT | `/api/v1/admin/products/{id}/` | Update product | Admin |
| DELETE | `/api/v1/admin/products/{id}/` | Delete product | Admin |

### Admin - Orders (`/api/v1/admin/orders/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/admin/orders/` | List all orders | Admin |
| GET | `/api/v1/admin/orders/{id}/` | Get order details | Admin |
| PATCH | `/api/v1/admin/orders/{id}/` | Update order status | Admin |

### Public - Categories (`/api/v1/categories/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/categories/` | List categories | No |
| GET | `/api/v1/categories/{slug}/` | Get category | No |

### Public - Products (`/api/v1/products/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/products/` | List active products | No |
| GET | `/api/v1/products/?category__slug={slug}` | Filter by category | No |
| GET | `/api/v1/products/?search={query}` | Search products | No |
| GET | `/api/v1/products/{slug}/` | Get product details | No |

### Customer - Orders (`/api/v1/orders/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/orders/` | List user's orders | Customer |
| POST | `/api/v1/orders/` | Create new order | Customer |
| GET | `/api/v1/orders/{id}/` | Get order details | Customer |

## Example Requests

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "username": "customer1",
    "password": "SecurePass123",
    "password2": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "customer"
  }'
```

### 2. Admin Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin-password"
  }'
```

### 3. Create Category (Admin)
```bash
curl -X POST http://localhost:8000/api/v1/admin/categories/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Electronics",
    "description": "Electronic devices and accessories"
  }'
```

### 4. Create Product (Admin)
```bash
curl -X POST http://localhost:8000/api/v1/admin/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "category": "CATEGORY_UUID",
    "name": "Wireless Headphones",
    "description": "Premium noise-cancelling headphones",
    "price": "199.99",
    "stock_quantity": 50,
    "image_url": "https://example.com/image.jpg"
  }'
```

### 5. Browse Products (Public)
```bash
curl http://localhost:8000/api/v1/products/
curl http://localhost:8000/api/v1/products/?category__slug=electronics
curl http://localhost:8000/api/v1/products/?search=headphones
```

### 6. Create Order (Customer)
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "shipping_address": "123 Main St, City, Country",
    "items": [
      {
        "product": "PRODUCT_UUID",
        "quantity": 2
      }
    ]
  }'
```

## Database Schema

### User Model
- UUID primary key
- Email (unique, username field)
- Role (admin/customer)
- Standard Django user fields

### Category Model
- UUID primary key
- Name (unique)
- Auto-generated slug
- Description

### Product Model
- UUID primary key
- Foreign key to Category
- Name, description, price
- Stock quantity
- Image URL
- Active status
- Auto-generated unique slug

### Order Model
- UUID primary key
- Foreign key to User (customer)
- Status (pending/processing/completed/cancelled)
- Total amount (auto-calculated)
- Shipping address
- Timestamps

### OrderItem Model
- UUID primary key
- Foreign keys to Order and Product
- Quantity
- Price at purchase (locked)
- Auto-calculated subtotal

## Security Features

- JWT token-based authentication
- Role-based access control (admin vs customer)
- Password validation and hashing
- CORS configuration for frontend integration
- Protected admin endpoints
- Order ownership verification

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production-grade WSGI server (gunicorn)
4. Configure PostgreSQL with proper credentials
5. Set up HTTPS/SSL
6. Configure static file serving
7. Set strong `SECRET_KEY`

## License

This project is for educational and commercial use.

## Support

For issues or questions, please contact the development team.
