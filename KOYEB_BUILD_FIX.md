# 🔧 Koyeb Build Fix - Exit Status 127

## The Problem
Exit status 127 means "command not found" - Koyeb can't execute the build.sh script.

## ✅ Solution: Don't Use build.sh

Instead of using `./build.sh` as the build command, configure it directly in Koyeb.

---

## 🎯 Updated Koyeb Configuration

### In Your Koyeb Dashboard:

**1. Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input
```

**Important Notes:**
- ❌ **Don't use**: `./build.sh`
- ❌ **Don't include**: `python manage.py migrate` in build (do it manually after first deploy)
- ✅ **Use**: Direct pip install command

**2. Run Command:**
```bash
gunicorn ecommerce_project.wsgi:application
```

**3. Environment Variables:**
Make sure ALL these are set:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | `i0m%r$+l&4x9rn4nimx@q5b%_c*7(atd*y968tc2im7dz&-ywv` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `*` |
| `TURSO_DATABASE_URL` | `https://womaclothes-mohamedghaly.aws-ap-northeast-1.turso.io` |
| `TURSO_AUTH_TOKEN` | `eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJleHAiOjE3OTYwMjYzNjMsImlhdCI6MTc2NDQ5MDM2MywiaWQiOiJkNWE3YTQ4NS0wZTFhLTRmZGYtYThlMi1lYzg3YzA5NzU5MTIiLCJyaWQiOiI1ZmY1MTU1NS0zNDI2LTRlMDAtYmFjNy02Yjg3OGQ1NWIxOTcifQ.GcwFibhXQ8VTtiBB9L7S1Thv0gUqGNUV6-o4IIAklc_Q8w80-6sx8jouMUHZeE7T7bkV18P5BqOtRdKCg-uaDg` |

---

## 📋 Step-by-Step Fix

### Option 1: Update Existing Service

1. Go to your Koyeb service
2. Click **"Settings"** or **"Edit Service"**
3. Under **"Builder"** section:
   - **Build command**: `pip install -r requirements.txt && python manage.py collectstatic --no-input`
   - **Run command**: `gunicorn ecommerce_project.wsgi:application`
4. Verify all environment variables are set
5. Click **"Update Service"** or **"Redeploy"**

### Option 2: Create New Service (Recommended)

1. Delete the current failing service
2. Click **"Create Web Service"**
3. Select **GitHub** → `Mohamedghaly/WomaBackend`
4. Configure as shown above
5. Click **"Deploy"**

---

## 🐛 Alternative: Even Simpler Build

If the above still fails, try this **minimal build command**:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Run Command:**
```bash
gunicorn ecommerce_project.wsgi:application
```

Then run migrations manually after deployment using Koyeb's console.

---

## 🔍 Common Issues

### Issue: "pip: command not found"
- Make sure `.python-version` file exists with `3.9`
- Koyeb should auto-detect Python and install pip

### Issue: "gunicorn: command not found"
- Make sure `gunicorn==21.2.0` is in `requirements.txt` ✅ (it is)

### Issue: "collectstatic failed"
- Make sure environment variables are set BEFORE building
- Especially `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN`

---

## 🎯 What Should Happen

Successful build logs should show:
```
✅ Detecting Python 3.9
✅ Installing pip dependencies
✅ Collecting static files
✅ Build complete
✅ Starting gunicorn
```

---

## 📞 If Still Failing

Share the **complete build logs** from Koyeb, especially:
1. The Python detection phase
2. The pip install output
3. The exact error message before "exit status 127"

This will help me identify the specific command that's failing.
