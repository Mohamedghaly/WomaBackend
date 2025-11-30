# Deploy Django Backend to Koyeb

This guide will walk you through deploying your Django backend to Koyeb.

## Prerequisites

- Koyeb account (sign up at [koyeb.com](https://koyeb.com))
- GitHub account with your code pushed to a repository
- Turso database credentials (already configured in your project)

## Step 1: Prepare Your Repository

Your repository is already configured with:
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python version specification
- ✅ `Procfile` - Gunicorn start command
- ✅ `build.sh` - Build script for migrations and static files
- ✅ WhiteNoise configured for static files

## Step 2: Push to GitHub

Make sure all your changes are committed and pushed:

```bash
git add .
git commit -m "Prepare for Koyeb deployment"
git push origin main
```

## Step 3: Deploy on Koyeb

1. **Go to Koyeb Dashboard**
   - Visit [app.koyeb.com](https://app.koyeb.com)
   - Click **Create Web Service**

2. **Select Deployment Method**
   - Choose **GitHub** as the deployment option
   - Select your repository: `Mohamedghaly/WomaBackend`
   - Select branch: `main`

3. **Builder Configuration**
   - Keep **Buildpack** selected (auto-detects Python)
   - **Build command**: `./build.sh`
   - **Run command**: `gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:$PORT`

4. **Configure Environment Variables**
   
   Click **Add Variable** and add the following:

   | Variable Name | Value |
   |--------------|-------|
   | `SECRET_KEY` | Generate a random string (use Django's `get_random_secret_key()`) |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `*` (or your specific Koyeb domain) |
   | `TURSO_DATABASE_URL` | `https://womaclothes-mohamedghaly.aws-ap-northeast-1.turso.io` |
   | `TURSO_AUTH_TOKEN` | Your Turso auth token |
   | `PYTHON_VERSION` | `3.9.0` |

5. **Service Configuration**
   - **Service name**: `woma-backend` (or your preferred name)
   - **Region**: Choose the closest to your users
   - **Instance type**: Start with the free tier (Nano)

6. **Deploy**
   - Click **Deploy** button
   - Wait for the build and deployment to complete (usually 2-5 minutes)

## Step 4: Verify Deployment

Once deployed, Koyeb will provide you with a URL like:
```
https://woma-backend-YOUR-ORG.koyeb.app
```

Test your API:
```bash
curl https://woma-backend-YOUR-ORG.koyeb.app/api/v1/
```

## Step 5: Update Frontend Configuration

Update your frontend API URL to point to your new Koyeb deployment:

```javascript
// In dashboard/js/api.js
const API_BASE_URL = 'https://woma-backend-YOUR-ORG.koyeb.app/api/v1';
```

## Continuous Deployment

Koyeb automatically redeploys your application whenever you push changes to your GitHub repository's main branch.

## Troubleshooting

### Build Fails
- Check the build logs in Koyeb dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify `runtime.txt` has correct Python version

### Database Connection Issues
- Verify `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` are set correctly
- Check that the URL uses `https://` scheme (not `libsql://`)

### Static Files Not Loading
- Ensure `python manage.py collectstatic` runs in `build.sh`
- Verify WhiteNoise is configured in `settings.py`

### Application Won't Start
- Check the run command is correct: `gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:$PORT`
- Verify `ALLOWED_HOSTS` includes your Koyeb domain

## Useful Commands

Generate a new Django secret key:
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## Next Steps

- Set up custom domain (optional)
- Configure CORS for your frontend domain
- Set up monitoring and logging
- Configure auto-scaling (if needed)

## Support

- Koyeb Documentation: https://www.koyeb.com/docs
- Koyeb Community: https://community.koyeb.com
