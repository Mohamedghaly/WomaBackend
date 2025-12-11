# 🚀 Deploy Dashboard to Netlify

## Quick Deploy Guide

### Method 1: Deploy via Netlify Dashboard (Recommended)

1. **Go to Netlify**
   - Visit https://app.netlify.com
   - Sign in or create an account

2. **Import from Git**
   - Click **"Add new site"** → **"Import an existing project"**
   - Choose **"Deploy with GitHub"**
   - Authorize Netlify to access your GitHub account

3. **Select Repository**
   - Choose: `Mohamedghaly/WomaBackend`
   - Click on the repository

4. **Configure Build Settings**
   - **Base directory**: `dashboard`
   - **Build command**: Leave empty (no build needed)
   - **Publish directory**: `.` (current directory, since base is already dashboard)
   - **Branch to deploy**: `main`

5. **Deploy!**
   - Click **"Deploy site"**
   - Wait 1-2 minutes for deployment
   - Your dashboard will be live!

---

### Method 2: Drag & Drop Deploy

1. **Go to Netlify**
   - Visit https://app.netlify.com

2. **Drag & Drop**
   - Scroll down to "Want to deploy a new site without connecting to Git?"
   - Drag the `dashboard` folder directly to the drop zone
   - Wait for upload and deployment

---

## 📋 Configuration Details

### Files Already Configured

✅ **`netlify.toml`** - Netlify configuration file
- Publish directory: `dashboard`
- Security headers configured
- Redirect rules set up

✅ **`dashboard/js/api.js`** - API URL updated
- Production: `https://warm-hippopotamus-ghaly-fafb8bcd.koyeb.app/api/v1`
- Local: `http://localhost:8000/api/v1`

---

## 🔗 After Deployment

### Your Dashboard URL
Netlify will give you a URL like:
```
https://YOUR-SITE-NAME.netlify.app
```

### Custom Domain (Optional)
1. Go to **Site settings** → **Domain management**
2. Click **"Add custom domain"**
3. Follow the instructions to configure your domain

---

## ✅ Verification Steps

After deployment, test these pages:

1. **Login Page**
   - `https://YOUR-SITE-NAME.netlify.app/`
   - Should show login form

2. **Dashboard** (after login)
   - `https://YOUR-SITE-NAME.netlify.app/dashboard.html`
   - Should show stats and overview

3. **Products Page**
   - `https://YOUR-SITE-NAME.netlify.app/products.html`
   - Should load products from your backend

4. **Categories Page**
   - `https://YOUR-SITE-NAME.netlify.app/categories.html`
   - Should load categories

5. **Orders Page**
   - `https://YOUR-SITE-NAME.netlify.app/orders.html`
   - Should load orders

---

## 🔐 Test Login

Use your backend admin credentials:
- Email: (your admin email)
- Password: (your admin password)

If you haven't created an admin user yet, do it via Koyeb console:
```bash
python manage.py createsuperuser
```

---

## 🐛 Troubleshooting

### Issue: "Failed to fetch" or CORS errors

**Solution**: The backend CORS is already configured to allow Netlify domains.
Your `settings.py` has:
```python
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.netlify\.app$",
]
```

### Issue: Login not working

**Check**:
1. Backend is running: https://warm-hippopotamus-ghaly-fafb8bcd.koyeb.app/api/v1/
2. Admin user exists (create via `createsuperuser`)
3. Browser console for errors (F12)

### Issue: 404 on page refresh

**Solution**: Already handled by `netlify.toml` redirect rules.

---

## 🔄 Continuous Deployment

Once connected to GitHub:
- Every push to `main` branch automatically deploys
- Netlify builds and publishes in ~30 seconds
- No manual steps needed

---

## 📊 Netlify Features You Get

✅ **Free SSL/HTTPS** - Automatic
✅ **CDN** - Global edge network
✅ **Instant rollback** - If something breaks
✅ **Deploy previews** - For pull requests
✅ **Custom domains** - Free
✅ **Analytics** - Built-in (paid feature)

---

## 🎯 Next Steps After Deployment

1. **Test all pages** - Make sure everything works
2. **Create admin user** - If you haven't already
3. **Add products** - Test the full workflow
4. **Share the URL** - Your dashboard is live!

---

## 📞 Support

- **Netlify Docs**: https://docs.netlify.com
- **Netlify Community**: https://answers.netlify.com

---

**Ready to deploy?** Follow Method 1 above for the best experience! 🚀
