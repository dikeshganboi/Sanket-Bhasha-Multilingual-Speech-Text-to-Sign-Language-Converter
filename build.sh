#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; [nltk.download(x) for x in ['punkt','stopwords','averaged_perceptron_tagger','wordnet','omw-1.4']]"

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
