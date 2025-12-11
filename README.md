# WOMA E-commerce Backend API

Django REST Framework backend for the WOMA Sportswear e-commerce platform.

## 🚀 Features

### Core Functionality
- 🔐 JWT Authentication
- 📦 Product Management with Dynamic Variations
- 🏷️ Category Management
- 🛒 Order Processing
- 👥 User Management
- 🎨 Dynamic Website Settings API
- 📊 Admin Dashboard APIs

### Dynamic Variations System
- Multi-attribute product variations (Color, Size, etc.)
- Custom attributes support
- Stock management per variation
- Price adjustments
- Auto-generated variation names

## 📁 Project Structure

```
WomaBackend/
├── accounts/               # User authentication & management
├── core/                   # Utilities (Colors, Sizes, Delivery Locations)
├── orders/                 # Order processing
├── products/               # Product & variation management
├── ecommerce_project/      # Django project settings
├── docs/                   # 📚 Documentation
│   ├── admin/             # Admin guides
│   ├── deployment/        # Deployment guides
│   └── guides/            # Feature guides
├── scripts/                # 🛠️ Utility scripts
│   ├── setup/             # Setup scripts
│   └── utils/             # Admin & utility scripts
├── postman/                # API testing collections
├── manage.py
├── requirements.txt
└── README.md
```

## 🛠️ Tech Stack

- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: 
  - Development: SQLite
  - Production: Turso (libSQL)
- **Deployment**: Koyeb
- **Static Files**: WhiteNoise

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/woma-project.git
cd WomaBackend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configurations
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
# Or use the script:
python scripts/utils/create_admin.py
```

7. **Run development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/v1/`

## 🔑 Default Admin Credentials

For development:
- Email: `admin@woma.com`
- Password: `admin123`

> ⚠️ **IMPORTANT**: Change these credentials in production!

## 📚 API Documentation

### Base URL
- Development: `http://localhost:8000/api/v1`
- Production: `https://warm-hippopotamus-ghaly-fafb8bcd.koyeb.app/api/v1`

### Authentication Endpoints
```
POST   /auth/login/          # Login (get JWT)
POST   /auth/register/       # Register new user
GET    /auth/profile/        # Get user profile
POST   /auth/token/refresh/  # Refresh JWT token
```

### Products Endpoints
```
GET    /products/                    # List all products
GET    /products/{id}/               # Get product details
POST   /admin/products/              # Create product (admin)
PUT    /admin/products/{id}/         # Update product (admin)
DELETE /admin/products/{id}/         # Delete product (admin)
GET    /admin/variations/            # List variations (admin)
POST   /admin/variations/            # Create variation (admin)
```

### Categories Endpoints
```
GET    /categories/                  # List all categories
GET    /categories/{id}/             # Get category details
POST   /admin/categories/            # Create category (admin)
PUT    /admin/categories/{id}/       # Update category (admin)
DELETE /admin/categories/{id}/       # Delete category (admin)
```

### Orders Endpoints
```
GET    /admin/orders/                # List all orders (admin)
GET    /admin/orders/{id}/           # Get order details (admin)
PATCH  /admin/orders/{id}/           # Update order status (admin)
POST   /orders/                      # Create order
```

### Utilities Endpoints
```
GET    /colors/                      # List colors
POST   /colors/                      # Create color (admin)
GET    /sizes/                       # List sizes
POST   /sizes/                       # Create size (admin)
GET    /delivery-locations/          # List delivery locations
POST   /delivery-locations/          # Create location (admin)
```

### Website Settings Endpoints (NEW!)
```
GET    /settings/                    # Get website settings
PUT    /admin/settings/              # Update settings (admin)
```

### Stats Endpoints
```
GET    /stats/                       # Get dashboard statistics (admin)
```

## 🧪 Testing

### Using Postman
Import the collections from `postman/` folder:
- API Collection: `Woma_Ecommerce_API.postman_collection.json`
- Environment: `Woma_Ecommerce_API.postman_environment.json`

### Running Tests
```bash
python manage.py test
```

## 🚀 Deployment

### Environment Variables
```env
# Database
TURSO_DATABASE_URL=your_turso_url
TURSO_AUTH_TOKEN=your_turso_token

# Django
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=your-domain.com

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.netlify.app
```

### Deployment to Koyeb

1. **Connect GitHub repository**
2. **Set build command**: `pip install -r requirements.txt`
3. **Set run command**: `gunicorn ecommerce_project.wsgi:application`
4. **Add environment variables**
5. **Deploy**

See `docs/deployment/` for detailed guides.

## 📊 Database Schema

### Core Models
- **User** - Custom user model with email authentication
- **Product** - Main product model
- **ProductVariation** - Dynamic variations with attributes
- **Category** - Product categories
- **Order** - Customer orders
- **OrderItem** - Items in orders
- **Color, Size, DeliveryLocation** - Utilities
- **WebsiteSettings** - Dynamic website configuration

## 🔧 Utilities & Scripts

### Setup Scripts (`scripts/setup/`)
- `setup.sh` - Initial project setup
- `setup_admin.sh` - Create admin user
- `build.sh` - Build script for deployment

### Admin Scripts (`scripts/utils/`)
- `create_admin.py` - Create superuser programmatically
- `create_sample_variations.py` - Generate sample data
- `check_env.py` - Validate environment variables
- `test_turso_connection.py` - Test Turso database connection
- `image_extractor.py` - Extract images from products

## 📖 Documentation

Comprehensive documentation available in `docs/`:

### Admin Guides
- Admin credentials management
- Quick reference for admin tasks
- Turso admin setup

### Deployment Guides
- Koyeb deployment
- Netlify deployment
- Production API guide
- Environment variables

### Feature Guides
- Dynamic variations system
- Custom variation names
- Stock management
- Image extraction
- Postman API testing

## 🔐 Security

- JWT-based authentication
- Token expiration and refresh
- Password hashing with Django's built-in system
- CORS configuration
- Environment-based settings
- Secure secret key management

## 🐛 Troubleshooting

Common issues and solutions in `docs/deployment/KOYEB_TROUBLESHOOTING.md`

### Common Commands
```bash
# Check environment
python scripts/utils/check_env.py

# Test database connection
python scripts/utils/test_turso_connection.py

# Create admin user
python scripts/utils/create_admin.py

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
```

## 📝 Development

### Code Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep views simple, logic in serializers/models

### Adding New Features
1. Create feature branch
2. Add models if needed
3. Create serializers
4. Add views
5. Register URLs
6. Test thoroughly
7. Update documentation
8. Submit PR

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📞 Support

For support, email support@woma.com

## 📄 License

This project is proprietary and confidential.

## 🎯 Recent Updates

### v2.0.0 - Website Settings API (December 2024)
- ✅ Added dynamic website settings system
- ✅ 29 customizable website fields
- ✅ Theme colors API
- ✅ Content management API
- ✅ SEO settings API

### v1.5.0 - Dynamic Variations (November 2024)
- ✅ Multi-attribute variation system
- ✅ Custom attributes support
- ✅ Auto-generated variation names
- ✅ Stock management per variation

## 🔗 Related Projects

- **Frontend**: WomaWebsite (React + TypeScript)
- **Dashboard**: Integrated into WomaWebsite
- **Deployment**: Koyeb (Backend) + Netlify (Frontend)

---

**Built with ❤️ by the WOMA Team**
