# Woma E-commerce Backend - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Navigate to Project
```bash
cd /Users/mohamedghaly/Desktop/WomaBackend
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations (Already Done)
```bash
python manage.py migrate
```

### 5. Create Admin User
```bash
python manage.py createsuperuser
```

Follow the prompts:
- Email: admin@woma.com
- Username: admin
- Password: (choose a secure password)
- First name: Admin
- Last name: User

When prompted for role, the superuser will default to admin.

### 6. Start Development Server
```bash
python manage.py runserver
```

Server will start at: `http://localhost:8000`

---

## 📚 Access Points

### API Documentation
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Django Admin Panel
- **URL**: http://localhost:8000/admin/
- **Login**: Use the superuser credentials you just created

---

## 🧪 Quick Test

### 1. Test User Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@customer.com",
    "username": "testcustomer",
    "password": "TestPass123",
    "password2": "TestPass123",
    "first_name": "Test",
    "last_name": "Customer",
    "role": "customer"
  }'
```

### 2. Test Admin Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@woma.com",
    "password": "your-password"
  }'
```

Copy the `access` token from the response for use in authenticated requests.

### 3. Create a Category (Admin)
```bash
curl -X POST http://localhost:8000/api/v1/admin/categories/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Electronics",
    "description": "Electronic devices and accessories"
  }'
```

### 4. Browse Categories (Public)
```bash
curl http://localhost:8000/api/v1/categories/
```

---

## 📱 Using Django Admin (Recommended for Quick Testing)

1. Go to http://localhost:8000/admin/
2. Login with your superuser credentials
3. Create categories and products directly in the admin interface
4. Test the API endpoints with the created data

The admin interface provides:
- User management
- Category CRUD
- Product CRUD with inventory management
- Order viewing and status updates

---

## 🗂️ Project Structure

```
WomaBackend/
├── accounts/          # User authentication
├── products/          # Products & categories
├── orders/            # Order management
├── ecommerce_project/ # Django settings
├── manage.py          # Django CLI
├── requirements.txt   # Dependencies
└── README.md          # Full documentation
```

---

## 📖 Full Documentation

- **README.md**: Complete API documentation with examples
- **walkthrough.md**: Detailed implementation walkthrough

---

## 🔧 Database Configuration

**Current**: SQLite (for easy testing)

**For PostgreSQL** (production):
1. Create PostgreSQL database
2. Create `.env` file:
   ```
   USE_POSTGRES=True
   DB_NAME=woma_ecommerce
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=5432
   ```
3. Run migrations again

---

## ✅ Verify Installation

```bash
python manage.py check
# Should output: System check identified no issues (0 silenced).
```

---

## 🎯 Next Steps

1. Create test data using Django admin
2. Test API endpoints using Swagger UI
3. Build a frontend application
4. Deploy to production

**Happy coding! 🚀**
