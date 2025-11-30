# 🎯 Netlify Deployment - Quick Start

## ✅ Pre-Deployment Checklist

- [x] Backend deployed to Koyeb ✅
- [x] API URL updated in dashboard ✅
- [x] Netlify configuration file created ✅
- [x] Changes pushed to GitHub ✅

---

## 🚀 Deploy Now (3 Steps)

### Step 1: Go to Netlify
Visit: **https://app.netlify.com**

### Step 2: Import Project
1. Click **"Add new site"** → **"Import an existing project"**
2. Choose **"Deploy with GitHub"**
3. Select repository: **`Mohamedghaly/WomaBackend`**

### Step 3: Configure
- **Base directory**: `dashboard`
- **Build command**: (leave empty)
- **Publish directory**: `.`
- Click **"Deploy site"**

---

## 🎉 That's It!

Your dashboard will be live in ~2 minutes at:
```
https://YOUR-SITE-NAME.netlify.app
```

---

## 🔗 Your Production Stack

| Component | URL |
|-----------|-----|
| **Backend API** | https://warm-hippopotamus-ghaly-fafb8bcd.koyeb.app |
| **Admin Dashboard** | https://YOUR-SITE-NAME.netlify.app |
| **Database** | Turso (libsql) |

---

## 📝 After Deployment

1. **Test Login**: Use your admin credentials
2. **Create Admin User** (if needed):
   ```bash
   # In Koyeb console
   python manage.py createsuperuser
   ```
3. **Test All Pages**: Products, Categories, Orders

---

## 📚 Full Guide

See `NETLIFY_DEPLOY.md` for detailed instructions and troubleshooting.

---

**Ready? Go to https://app.netlify.com and deploy!** 🚀
