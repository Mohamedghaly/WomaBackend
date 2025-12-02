#!/bin/bash

echo "=== Turso Database Credentials Retrieval ==="
echo ""

# Check if turso CLI is installed
if ! command -v turso &> /dev/null; then
    echo "❌ Turso CLI is not installed."
    echo ""
    echo "Install it with one of these commands:"
    echo "  brew install tursodatabase/tap/turso"
    echo "  OR"
    echo "  curl -sSfL https://get.tur.so/install.sh | bash"
    exit 1
fi

echo "✅ Turso CLI is installed"
echo ""

# Check if user is logged in
if ! turso auth status &> /dev/null; then
    echo "❌ Not logged into Turso. Please login:"
    echo "  turso auth login"
    exit 1
fi

echo "✅ Logged into Turso"
echo ""

# List databases
echo "📊 Your Turso Databases:"
turso db list
echo ""

# Prompt for database name
echo "Enter your database name (or press Enter for 'womaclothes'):"
read -r DB_NAME
DB_NAME=${DB_NAME:-womaclothes}

echo ""
echo "Getting credentials for database: $DB_NAME"
echo ""

# Get database URL
echo "📍 Database URL:"
DB_URL=$(turso db show $DB_NAME --url 2>/dev/null)
if [ -z "$DB_URL" ]; then
    echo "❌ Could not find database '$DB_NAME'"
    echo "Available databases:"
    turso db list
    exit 1
fi
echo "$DB_URL"
echo ""

# Create new token
echo "🔑 Creating new auth token..."
AUTH_TOKEN=$(turso db tokens create $DB_NAME 2>/dev/null)
if [ -z "$AUTH_TOKEN" ]; then
    echo "❌ Could not create token for '$DB_NAME'"
    exit 1
fi
echo "Token created successfully (first 20 chars): ${AUTH_TOKEN:0:20}..."
echo ""

# Display the .env format
echo "=== Add these to your .env file ==="
echo ""
echo "TURSO_DATABASE_URL=$DB_URL"
echo "TURSO_AUTH_TOKEN=$AUTH_TOKEN"
echo ""
echo "=== Copy the above lines to your .env file ==="
