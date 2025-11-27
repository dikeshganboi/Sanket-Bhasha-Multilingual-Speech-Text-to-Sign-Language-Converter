#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt', download_dir='/opt/render/nltk_data'); nltk.download('stopwords', download_dir='/opt/render/nltk_data'); nltk.download('averaged_perceptron_tagger', download_dir='/opt/render/nltk_data'); nltk.download('wordnet', download_dir='/opt/render/nltk_data'); nltk.download('omw-1.4', download_dir='/opt/render/nltk_data')"

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
