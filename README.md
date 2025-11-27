# 🌍 Sanket Bhasha - Multilingual Speech/Text to Sign Language Converter

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://sanket-bhasha-isl.onrender.com)
[![Python](https://img.shields.io/badge/python-3.11.9-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.1.13-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Convert text and voice from **12+ Indian languages** into Indian Sign Language (ISL) animations with real-time translation and natural language processing.

🔗 **Live Application**: [https://sanket-bhasha-isl.onrender.com](https://sanket-bhasha-isl.onrender.com)

## ✨ Features

- 🗣️ **Multilingual Support** - Hindi, Gujarati, Marathi, Bengali, Tamil, Telugu, Kannada, Malayalam, Punjabi, Urdu, and more
- 🎤 **Speech-to-Text** - Real-time voice input with language detection
- 🔊 **Text-to-Speech** - Audio playback in multiple Indian languages
- 🤖 **NLP Processing** - Advanced tokenization, lemmatization, and POS tagging
- 🎬 **ISL Animations** - 150+ sign language video animations
- 🔐 **User Authentication** - Secure signup/login system
- 📱 **Responsive Design** - Mobile-friendly interface with Tailwind CSS

## 🛠️ Tech Stack

- **Backend**: Django 4.1.13, Python 3.11.9
- **NLP**: NLTK, langdetect, WordNet
- **Translation**: googletrans 3.1.0a0
- **Frontend**: Tailwind CSS, JavaScript
- **Database**: SQLite (dev), PostgreSQL (production)
- **Deployment**: Render.com, Gunicorn, Whitenoise

## 🚀 Local Development

### Prerequisites

- Python 3.11.9+
- pip

### Setup

```bash
# 1. Clone repository
git clone https://github.com/dikeshganboi/Sanket-Bhasha-Multilingual-Speech-Text-to-Sign-Language-Converter.git
cd Sanket-Bhasha-Multilingual-Speech-Text-to-Sign-Language-Converter

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet'); nltk.download('omw-1.4')"

# 5. Setup environment variables
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
# Edit .env and add your SECRET_KEY

# 6. Run migrations
python manage.py migrate

# 7. Create superuser (optional)
python manage.py createsuperuser

# 8. Collect static files
python manage.py collectstatic

# 9. Run development server
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## 📂 Project Structure

```
A2SL/                    # Django project configuration
  ├── settings.py        # Project settings
  ├── urls.py            # URL routing
  ├── views.py           # View logic
  └── translation_service.py  # Translation utilities
assets/                  # ISL animation videos (150+ MP4 files)
static/                  # Static assets (CSS, images)
templates/               # HTML templates
  ├── home.html          # Landing page
  ├── animation.html     # Main converter interface
  ├── login.html         # Authentication
  └── signup.html
tests/                   # Test suite
requirements.txt         # Python dependencies
Procfile                 # Deployment configuration
runtime.txt              # Python version
build.sh                 # Build script
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_integration.py

# Run with coverage
pytest --cov=A2SL
```

## 🔒 Environment Variables

Create `.env` file based on `.env.example`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3  # or PostgreSQL URL
```

## 🚀 Production Deployment

Deployed on [Render.com](https://render.com) with:

- ✅ **Gunicorn** - Production WSGI server
- ✅ **Whitenoise** - Static file serving
- ✅ **PostgreSQL** - Production database support
- ✅ **SSL/HTTPS** - Secure connections
- ✅ **Auto-deploy** - CI/CD from GitHub

### Deploy to Render

1. Fork this repository
2. Create new Web Service on [Render](https://render.com)
3. Connect your GitHub repository
4. Render will auto-detect settings from `render.yaml`
5. Add environment variables:
   - `SECRET_KEY` - Generate secure key
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app.onrender.com`
6. Deploy automatically!

### One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Dikesh Ganboi**

- GitHub: [@dikeshganboi](https://github.com/dikeshganboi)
- Project: [Sanket Bhasha ISL Converter](https://github.com/dikeshganboi/Sanket-Bhasha-Multilingual-Speech-Text-to-Sign-Language-Converter)

## 🙏 Acknowledgments

- Indian Sign Language video assets
- NLTK and NLP community
- Django and Python communities
- All contributors and users

---

⭐ **Star this repo** if you find it helpful!

🌐 **Live Demo**: [https://sanket-bhasha-isl.onrender.com](https://sanket-bhasha-isl.onrender.com)
