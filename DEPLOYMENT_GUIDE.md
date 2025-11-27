# 🚀 Deployment Guide - Sanket Bhasha ISL Converter

This guide will help you deploy your Multilingual Text/Voice to Indian Sign Language (ISL) converter to production.

## ✅ Pre-Deployment Checklist

Your project is now production-ready with:

- ✅ Gunicorn (Production WSGI server)
- ✅ Whitenoise (Static file serving)
- ✅ Python-decouple (Environment variable management)
- ✅ Security settings configured
- ✅ Static files collection setup
- ✅ Database migrations ready

## 🌐 Deployment Options

### Option 1: Deploy to Render (Recommended - Free Tier Available)

**Why Render?**

- Free tier available
- Easy PostgreSQL integration
- Automatic deployments from Git
- No credit card required for free tier

**Steps:**

1. **Push your code to GitHub:**

   ```bash
   git init
   git add .
   git commit -m "Initial commit - Ready for deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Create a Render account:**

   - Go to https://render.com
   - Sign up with GitHub

3. **Create a new Web Service:**

   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** sanket-bhasha-isl
     - **Environment:** Python 3
     - **Build Command:** `./build.sh`
     - **Start Command:** `gunicorn A2SL.wsgi:application`

4. **Add Environment Variables:**
   Go to "Environment" tab and add:

   ```
   SECRET_KEY=<generate-a-new-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   DATABASE_ENGINE=django.db.backends.postgresql
   DATABASE_NAME=sanket_bhasha_db
   DATABASE_USER=<will-be-provided-by-render>
   DATABASE_PASSWORD=<will-be-provided-by-render>
   DATABASE_HOST=<will-be-provided-by-render>
   DATABASE_PORT=5432
   ```

5. **Add PostgreSQL Database (Optional but recommended):**

   - Create new PostgreSQL database on Render
   - Copy connection details to environment variables

6. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app

**Generate a new SECRET_KEY:**

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### Option 2: Deploy to Railway (Easy Alternative)

**Steps:**

1. **Install Railway CLI:**

   ```bash
   npm i -g @railway/cli
   ```

2. **Login and Initialize:**

   ```bash
   railway login
   railway init
   ```

3. **Add PostgreSQL:**

   ```bash
   railway add
   # Select PostgreSQL
   ```

4. **Set Environment Variables:**

   ```bash
   railway variables set SECRET_KEY="your-secret-key"
   railway variables set DEBUG="False"
   railway variables set ALLOWED_HOSTS="your-app.railway.app"
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

---

### Option 3: Deploy to Heroku

**Steps:**

1. **Install Heroku CLI:**

   - Download from https://devcenter.heroku.com/articles/heroku-cli

2. **Login and Create App:**

   ```bash
   heroku login
   heroku create sanket-bhasha-isl
   ```

3. **Add PostgreSQL:**

   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set Environment Variables:**

   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG="False"
   heroku config:set ALLOWED_HOSTS="your-app.herokuapp.com"
   ```

5. **Deploy:**

   ```bash
   git push heroku main
   ```

6. **Run Migrations:**
   ```bash
   heroku run python manage.py migrate
   ```

---

## 🔧 Post-Deployment Configuration

### 1. Update Settings for PostgreSQL (if using)

Update your `.env` file or environment variables:

```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=your_db_host
DATABASE_PORT=5432
```

Then update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DATABASE_NAME', default=os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': config('DATABASE_USER', default=''),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default=''),
        'PORT': config('DATABASE_PORT', default=''),
    }
}
```

### 2. Create Superuser

After deployment, create an admin user:

```bash
# For Render/Railway
python manage.py createsuperuser

# For Heroku
heroku run python manage.py createsuperuser
```

### 3. Verify Deployment

- Visit your deployed URL
- Test the ISL converter functionality
- Access admin panel at `/admin/`
- Check static files are loading correctly

---

## 🔒 Security Checklist

Before going live, ensure:

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` (never commit to Git)
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] HTTPS enabled (automatic on Render/Heroku)
- [ ] Database backups configured
- [ ] Environment variables secured

---

## 📊 Monitoring & Logs

**Render:**

```bash
# View logs in dashboard or CLI
render logs
```

**Railway:**

```bash
railway logs
```

**Heroku:**

```bash
heroku logs --tail
```

---

## 🐛 Troubleshooting

### Static Files Not Loading

1. Ensure `whitenoise` is installed
2. Run `python manage.py collectstatic`
3. Check `STATICFILES_STORAGE` setting

### Database Connection Errors

1. Verify environment variables
2. Check database credentials
3. Ensure database addon is created

### 500 Internal Server Error

1. Check application logs
2. Verify `SECRET_KEY` is set
3. Ensure all environment variables are configured

---

## 🔄 Continuous Deployment

**GitHub Actions (Recommended):**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

---

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/)
- [Render Django Guide](https://render.com/docs/deploy-django)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)

---

## 🎉 Success!

Your ISL converter is now deployed and accessible to users worldwide!

**Next Steps:**

1. Share your deployment URL
2. Monitor application performance
3. Gather user feedback
4. Iterate and improve

---

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Review application logs
3. Verify environment variables
4. Test locally with production settings

**Local Production Test:**

```bash
# Set DEBUG=False in .env
python manage.py runserver
# Or test with gunicorn
gunicorn A2SL.wsgi:application
```
