# 🌍 Multilingual Text/Voice to Indian Sign Language (ISL) Converter

A Django-based web app that converts text and voice from 12+ Indian regional languages into Indian Sign Language (ISL) animations with real-time translation, NLP processing, and audio verification.

## ✨ Features

- 12+ language input with auto-detection
- Speech-to-text and Text-to-Speech (TTS)
- Real-time translation (googletrans)
- NLP pipeline (tokenize, lemmatize, POS tagging)
- ISL animation playback from local assets
- User auth (signup/login), admin dashboard

## 🧰 Tech Stack

- Backend: Python 3.8+, Django 4.1+
- NLP: NLTK, langdetect
- Translation: googletrans (client)
- Frontend: Django templates, Tailwind CSS
- Database: SQLite (dev)

## 🚀 Quickstart

```bash
# 1) Create venv
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) (optional) Download NLTK corpora
python -c "import nltk; [nltk.download(x) for x in ['punkt','stopwords','averaged_perceptron_tagger','wordnet','omw-1.4']]"

# 4) Configure env
copy .env.example .env   # on Windows
# cp .env.example .env   # on Linux/Mac

# 5) Migrate DB and run
python manage.py migrate
python manage.py runserver
```

Admin panel: `http://localhost:8000/admin/`

Create admin:

```bash
python manage.py createsuperuser
```

## 📂 Project Structure

```
A2SL/                    # Django project (settings, urls, views, translation)
assets/                  # ISL animation videos (mp4)
static/                  # CSS/JS/images
templates/               # HTML templates
scripts/                 # Utility scripts (DB/user helpers)
tests/                   # Test suite
README.md                # This file
requirements.txt         # Dependencies
```

## 🧪 Testing

```bash
pytest
# or
python tests/run_tests.py
```

## 🔒 Environment Variables (.env)

See `.env.example` for all variables.

Key settings:

- `SECRET_KEY` (required in production)
- `DEBUG` (True/False)
- `ALLOWED_HOSTS` (CSV list)
- `DATABASE_ENGINE`, `DATABASE_NAME`

## 🚀 Production Deployment

This project is **production-ready** with:

- ✅ Gunicorn WSGI server
- ✅ Whitenoise static file management
- ✅ Environment variable configuration
- ✅ PostgreSQL support
- ✅ Security settings enabled

### Quick Deploy

**See detailed guides:**

- `DEPLOYMENT_COMPLETE.md` - Status and overview
- `DEPLOYMENT_GUIDE.md` - Comprehensive deployment instructions
- `QUICK_DEPLOY.md` - Quick reference commands

**Recommended Platforms:**

- [Render.com](https://render.com) - Free tier, easy setup
- [Railway.app](https://railway.app) - Modern, simple deployment
- [Heroku](https://heroku.com) - Traditional, reliable

### One-Click Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

Use the included `render.yaml` for automatic configuration.

## 📜 License

See `LICENSE`.

## 🤝 Contributing

- Fork, create feature branch, open PR
- Add tests where possible
- Follow PEP8 and keep changes focused

---

For detailed feature docs, see `docs/` and `README_MULTILINGUAL.md`.
