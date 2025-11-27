# Quick Deployment Commands

## For Render.com (Recommended)

### 1. Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Git Setup

```bash
git init
git add .
git commit -m "Ready for deployment"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 3. Render Dashboard Setup

1. Go to https://render.com/dashboard
2. New → Web Service
3. Connect your GitHub repository
4. Settings:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn A2SL.wsgi:application`

### 4. Environment Variables (Add in Render)

```
SECRET_KEY=<from-step-1>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

---

## For Railway.app (Alternative)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Add PostgreSQL (optional)
railway add

# Set variables
railway variables set SECRET_KEY="your-secret-key"
railway variables set DEBUG="False"

# Deploy
railway up

# Open in browser
railway open
```

---

## For Heroku (Traditional)

```bash
# Login
heroku login

# Create app
heroku create sanket-bhasha-isl

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set config
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG="False"

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Open app
heroku open
```

---

## Local Testing Before Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Test with Django dev server
python manage.py runserver

# Or test with Gunicorn
gunicorn A2SL.wsgi:application
```

---

## Create Superuser (After Deployment)

**Render/Railway:**
Use the web console in dashboard or:

```bash
python manage.py createsuperuser
```

**Heroku:**

```bash
heroku run python manage.py createsuperuser
```

---

## Check Logs

**Render:** Dashboard → Logs tab

**Railway:**

```bash
railway logs
```

**Heroku:**

```bash
heroku logs --tail
```
