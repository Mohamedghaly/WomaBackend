# Deployment Guide

## Part 1: Deploy Backend (Render)

1.  Go to [dashboard.render.com](https://dashboard.render.com/)
2.  Click **New +** -> **Web Service**
3.  Connect your GitHub repository: `Mohamedghaly/WomaBackend`
4.  Configure the service:
    *   **Name:** `woma-backend` (or similar)
    *   **Runtime:** `Python 3`
    *   **Build Command:** `./build.sh`
    *   **Start Command:** `gunicorn ecommerce_project.wsgi:application`
5.  **Environment Variables:**
    *   Add `PYTHON_VERSION` = `3.9.0` (or your local version)
    *   Add `SECRET_KEY` = (Generate a random string)
    *   Add `DEBUG` = `False`
    *   Add `ALLOWED_HOSTS` = `*`
6.  Click **Create Web Service**

**Wait for the deploy to finish.** Copy your backend URL (e.g., `https://woma-backend-xyz.onrender.com`).

## Part 2: Update Frontend Config

1.  Open `dashboard/js/api.js` in your code.
2.  Update line 4 with your **actual** Render URL:
    ```javascript
    : 'https://your-render-url.onrender.com/api/v1';
    ```
3.  Commit and push this change:
    ```bash
    git add dashboard/js/api.js
    git commit -m "Update API URL"
    git push origin main
    ```

## Part 3: Deploy Frontend (Netlify)

1.  Go to [app.netlify.com](https://app.netlify.com/)
2.  Click **Add new site** -> **Import from Git**
3.  Connect GitHub and choose `WomaBackend`
4.  Configure build settings:
    *   **Base directory:** `dashboard`
    *   **Build command:** (Leave empty)
    *   **Publish directory:** `.` (or leave empty to publish the base directory)
5.  Click **Deploy site**

## Done! 🚀
Your admin dashboard will be live on Netlify, connected to your Django backend on Render and Turso database.
