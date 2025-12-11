#!/bin/bash

# Woma E-commerce Backend Setup Script

echo "🚀 Setting up Woma E-commerce Backend..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Create virtual environment
echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
python3 -m venv venv

# Step 2: Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Step 3: Upgrade pip
echo -e "${YELLOW}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip

# Step 4: Install dependencies
echo -e "${YELLOW}📚 Installing dependencies...${NC}"
pip install -r requirements.txt

# Step 5: Create .env file if not exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created. Please update it with your database credentials.${NC}"
else
    echo -e "${GREEN}✅ .env file already exists.${NC}"
fi

# Step 6: Run migrations
echo -e "${YELLOW}🗄️  Creating database migrations...${NC}"
python manage.py makemigrations

echo -e "${YELLOW}🗄️  Running database migrations...${NC}"
python manage.py migrate

echo -e "${GREEN}✨ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Create a superuser: python manage.py createsuperuser"
echo "2. Run the development server: python manage.py runserver"
echo "3. Visit API docs: http://localhost:8000/api/schema/swagger-ui/"
