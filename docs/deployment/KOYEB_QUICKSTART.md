# 🚀 Koyeb Deployment - Quick Start

Your Django backend is ready to deploy to Koyeb! Here's everything you need.

## 📦 What's Been Configured

✅ **Database**: Turso (already connected and tested)
✅ **Static Files**: WhiteNoise configured
✅ **CORS**: Set up for local + production domains
✅ **Build Script**: `build.sh` ready
✅ **Runtime**: Python 3.9.0 specified
✅ **Web Server**: Gunicorn configured
✅ **Secret Key**: Generated for production

## 🎯 Quick Deploy (5 Steps)

### Step 1: Commit & Push
```bash
cd /Users/mohamedghaly/Desktop/WomaBackend
git add .
git commit -m "Configure for Koyeb deployment"
git push origin main
```

### Step 2: Create Koyeb Service
1. Go to https://app.koyeb.com
2. Click **"Create Web Service"**
3. Select **GitHub**
4. Choose repo: `Mohamedghaly/WomaBackend`
5. Branch: `main`

### Step 3: Configure Build
- **Build command**: `./build.sh`
- **Run command**: `gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:$PORT`

### Step 4: Add Environment Variables

Click "Add variable" for each:

| Name | Value |
|------|-------|
| `SECRET_KEY` | `i0m%r$+l&4x9rn4nimx@q5b%_c*7(atd*y968tc2im7dz&-ywv` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `*` |
| `TURSO_DATABASE_URL` | `https://womaclothes-mohamedghaly.aws-ap-northeast-1.turso.io` |
| `TURSO_AUTH_TOKEN` | `eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJleHAiOjE3OTYwMjYzNjMsImlhdCI6MTc2NDQ5MDM2MywiaWQiOiJkNWE3YTQ4NS0wZTFhLTRmZGYtYThlMi1lYzg3YzA5NzU5MTIiLCJyaWQiOiI1ZmY1MTU1NS0zNDI2LTRlMDAtYmFjNy02Yjg3OGQ1NWIxOTcifQ.GcwFibhXQ8VTtiBB9L7S1Thv0gUqGNUV6-o4IIAklc_Q8w80-6sx8jouMUHZeE7T7bkV18P5BqOtRdKCg-uaDg` |
| `PYTHON_VERSION` | `3.9.0` |

### Step 5: Deploy!
Click **"Deploy"** and wait 2-5 minutes.

## ✅ Test Your Deployment

Once deployed, test your API:
```bash
# Replace YOUR-ORG with your actual Koyeb org name
curl https://woma-backend-YOUR-ORG.koyeb.app/api/v1/
```

## 📱 Update Your Frontend

Update your frontend's API URL:
```javascript
const API_BASE_URL = 'https://woma-backend-YOUR-ORG.koyeb.app/api/v1';
```

## 📚 Additional Resources

- **Full Guide**: See `KOYEB_DEPLOY.md` for detailed instructions
- **Checklist**: See `KOYEB_CHECKLIST.md` for step-by-step checklist
- **Env Vars**: See `KOYEB_ENV_VARS.md` for all environment variables

## 🆘 Need Help?

Common issues:
- **Build fails**: Check build logs in Koyeb dashboard
- **Can't connect to DB**: Verify TURSO_DATABASE_URL uses `https://`
- **Static files missing**: Ensure WhiteNoise is in MIDDLEWARE
- **CORS errors**: Check CORS_ALLOWED_ORIGINS in settings.py

## 🎉 That's It!

Your backend will be live at:
```
https://woma-backend-YOUR-ORG.koyeb.app
```

Koyeb will auto-deploy whenever you push to GitHub! 🚀
