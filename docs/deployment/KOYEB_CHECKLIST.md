# Koyeb Deployment Checklist

## ✅ Pre-Deployment (Completed)

- [x] Database configured (Turso)
- [x] `requirements.txt` present
- [x] `runtime.txt` created (Python 3.9.0)
- [x] `Procfile` created (Gunicorn command)
- [x] `build.sh` configured
- [x] WhiteNoise configured for static files
- [x] CORS settings updated for production
- [x] AUTH_USER_MODEL configured
- [x] Environment variables documented

## 📋 Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Configure for Koyeb deployment"
git push origin main
```

### 2. Create Koyeb Service
- Go to https://app.koyeb.com
- Click "Create Web Service"
- Select GitHub deployment
- Choose repository: `Mohamedghaly/WomaBackend`
- Branch: `main`

### 3. Configure Build
- **Build command**: `./build.sh`
- **Run command**: `gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:$PORT`

### 4. Add Environment Variables
Copy from `KOYEB_ENV_VARS.md`:
- SECRET_KEY
- DEBUG=False
- ALLOWED_HOSTS=*
- TURSO_DATABASE_URL
- TURSO_AUTH_TOKEN
- PYTHON_VERSION=3.9.0

### 5. Deploy
- Click "Deploy"
- Wait for build to complete (2-5 minutes)
- Note your deployment URL

### 6. Test Deployment
```bash
# Replace with your actual Koyeb URL
curl https://woma-backend-YOUR-ORG.koyeb.app/api/v1/
```

## 🔍 Post-Deployment Verification

- [ ] API responds at `/api/v1/`
- [ ] Admin panel accessible at `/admin/`
- [ ] Database connection working
- [ ] Static files loading correctly
- [ ] CORS working for frontend

## 📝 Next Steps

1. Update frontend API URL to point to Koyeb deployment
2. Test all API endpoints
3. Create superuser if needed:
   ```bash
   # In Koyeb console or via SSH
   python manage.py createsuperuser
   ```
4. Configure custom domain (optional)
5. Set up monitoring

## 🆘 Troubleshooting

If deployment fails, check:
- Build logs in Koyeb dashboard
- Environment variables are set correctly
- Database URL uses `https://` scheme
- All dependencies in `requirements.txt`

## 📚 Documentation

- Full guide: `KOYEB_DEPLOY.md`
- Environment variables: `KOYEB_ENV_VARS.md`
- Koyeb docs: https://www.koyeb.com/docs
