# Koyeb Build Error Troubleshooting

## Common Build Issues & Solutions

### Issue 1: Runtime.txt Format
**Try removing runtime.txt entirely** - Koyeb's buildpack should auto-detect Python from requirements.txt

```bash
# Option 1: Delete runtime.txt
rm runtime.txt

# Option 2: Or use this format instead
echo "3.9" > runtime.txt
```

### Issue 2: Build Command Issues
**In Koyeb Dashboard**, try these build command variations:

**Option A: Use pip directly (no build.sh)**
```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

**Option B: Simplified build.sh**
```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
```
(Remove migrate from build - do it manually after deployment)

**Option C: No build command**
Leave build command empty and let Koyeb auto-detect

### Issue 3: Run Command
Make sure your run command is:
```bash
gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:$PORT
```

Or try without the bind:
```bash
gunicorn ecommerce_project.wsgi:application
```

### Issue 4: Missing Dependencies
Check if `libsql-client` is causing issues. Try this alternative requirements.txt:

```txt
Django==4.2.17
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
django-filter==24.1
drf-spectacular==0.27.0
python-dotenv==1.0.0
Pillow==10.2.0
gunicorn==21.2.0
whitenoise==6.6.0
libsql-client==0.3.1
```

### Issue 5: Python Version
Koyeb might not support Python 3.9.0 exactly. Try:
- Remove runtime.txt (let it auto-detect)
- Or use: `3.9` or `3.11` in runtime.txt

### Issue 6: Procfile Not Needed
Koyeb might not use Procfile. Instead:
1. Delete Procfile
2. Set the run command directly in Koyeb dashboard

## Step-by-Step Fix

### Quick Fix (Try This First):

1. **Remove runtime.txt**:
   ```bash
   git rm runtime.txt
   git commit -m "Remove runtime.txt"
   git push
   ```

2. **In Koyeb Dashboard**:
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --no-input`
   - Run command: `gunicorn ecommerce_project.wsgi:application`

3. **Redeploy**

### Alternative: Use Docker Instead

If buildpack keeps failing, use Docker deployment:

1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "ecommerce_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

2. In Koyeb, select "Docker" instead of "GitHub"
3. Build and push to Docker Hub, then deploy

## What to Check in Build Logs

Look for these specific errors:
- `Python version not found` → Remove runtime.txt
- `pip install failed` → Check requirements.txt
- `collectstatic failed` → Check STATIC_ROOT in settings
- `Module not found` → Missing dependency

## Share Your Build Logs

To get specific help, share:
1. The exact error message from Koyeb build logs
2. Which build command you're using
3. Your environment variables (without sensitive values)

## Quick Test Locally

Before deploying, test the build process locally:
```bash
# Test pip install
pip install -r requirements.txt

# Test collectstatic
python manage.py collectstatic --no-input

# Test gunicorn
gunicorn ecommerce_project.wsgi:application
```

If any of these fail locally, fix them first!
