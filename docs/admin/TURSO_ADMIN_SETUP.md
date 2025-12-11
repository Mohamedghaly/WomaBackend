# Turso Database Setup Guide

## Overview
You need to configure your Turso database credentials to create the admin user in the production database.

## Required Environment Variables

Your `.env` file should contain:

```env
# Turso Database Configuration
TURSO_DATABASE_URL=libsql://your-database-name.turso.io
TURSO_AUTH_TOKEN=your-turso-auth-token
```

## How to Get Your Turso Credentials

### 1. Install Turso CLI (if not already installed)
```bash
brew install tursodatabase/tap/turso
# or
curl -sSfL https://get.tur.so/install.sh | bash
```

### 2. Login to Turso
```bash
turso auth login
```

### 3. Get Your Database URL
```bash
turso db show womaclothes
```
Look for the URL field.

### 4. Create or Get Auth Token
```bash
turso db tokens create womaclothes
```

### 5. Update Your .env File
Add the values to `/Users/mohamedghaly/Desktop/WomaProject/WomaBackend/.env`:

```env
TURSO_DATABASE_URL=libsql://womaclothes-mohamedghaly.turso.io
TURSO_AUTH_TOKEN=eyJhbGc... (your token here)
```

## After Configuration

Once you've added the Turso credentials to your `.env` file, run:

```bash
cd /Users/mohamedghaly/Desktop/WomaProject/WomaBackend
python3 create_admin.py
```

This will create the admin account with:
- **Email:** admin@woma.com
- **Password:** admin123
- **Role:** admin

## Alternative: Use Local SQLite for Testing

If you want to test locally first before pushing to Turso, you can:

1. Comment out or remove `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` from `.env`
2. Run migrations: `python3 manage.py migrate`
3. Create admin: `python3 create_admin.py`

The system will automatically fall back to SQLite (`db.sqlite3`) when Turso credentials are not present.
