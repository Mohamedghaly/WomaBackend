# Turso Database Migration Guide

## Step 1: Install Turso CLI

```bash
# Install Turso CLI
brew install tursodatabase/tap/turso

# Or using curl:
curl -sSfL https://get.tur.so/install.sh | bash
```

## Step 2: Login to Turso

```bash
turso auth login
```

## Step 3: Create Your Database

```bash
# Create a new database
turso db create woma-backend

# Get the database URL
turso db show woma-backend --url

# Create an auth token
turso db tokens create woma-backend
```

## Step 4: Install Python Package

```bash
cd /Users/mohamedghaly/Desktop/WomaBackend
source venv/bin/activate
pip install django-turso
```

## Step 5: Update Django Settings

Add to `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_turso',
        'NAME': 'your-turso-db-url',
        'OPTIONS': {
            'authToken': 'your-turso-auth-token',
        }
    }
}
```

## Step 6: Migrate Data

```bash
# Run migrations on Turso
python manage.py migrate

# Export data from SQLite
python manage.py dumpdata > data_backup.json

# Load data into Turso
python manage.py loaddata data_backup.json
```

---

**Would you like me to:**
1. Walk you through this manually, or
2. Automate the setup (need your Turso credentials)?
