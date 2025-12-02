#!/bin/bash

echo "=== Woma Admin Account Setup ==="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your Turso credentials."
    echo ""
    echo "You can use: ./get_turso_credentials.sh to get your credentials"
    exit 1
fi

echo "✅ .env file found"
echo ""

# Check if Turso credentials are set (basic check)
if grep -q "TURSO_DATABASE_URL" .env && grep -q "TURSO_AUTH_TOKEN" .env; then
    echo "✅ Turso credentials found in .env"
    echo ""
    
    # Check if credentials have actual values (not placeholder)
    if grep -q "TURSO_DATABASE_URL=libsql://" .env; then
        echo "📊 Creating admin account in Turso database..."
    else
        echo "⚠️  TURSO_DATABASE_URL might not be properly set"
        echo "Make sure it looks like: TURSO_DATABASE_URL=libsql://your-db.turso.io"
        echo ""
        echo "Continuing anyway..."
    fi
else
    echo "⚠️  Turso credentials not found in .env"
    echo "The system will use local SQLite database instead."
    echo ""
    read -p "Continue with local SQLite? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled. Please add Turso credentials to .env first."
        exit 1
    fi
fi

echo ""
echo "🚀 Running create_admin.py..."
echo ""

# Run the admin creation script
python3 create_admin.py

echo ""
echo "=== Setup Complete ==="
echo ""
echo "If successful, you can now login to your dashboard with:"
echo "  Email: admin@woma.com"
echo "  Password: admin123"
