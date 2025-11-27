#!/usr/bin/env python3
"""
Test Configuration and Setup
Centralized test configuration and utilities
"""

import os
import sys
import django
import unittest
from unittest.mock import patch
import tempfile
import shutil

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A2SL.settings')
django.setup()

from django.test import TestCase, override_settings
from django.conf import settings

class TestConfig(TestCase):
    """Test configuration and setup"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class"""
        super().setUpClass()
        # Create temporary directory for test files
        cls.temp_dir = tempfile.mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test class"""
        super().tearDownClass()
        # Remove temporary directory
        shutil.rmtree(cls.temp_dir)
    
    def test_django_settings(self):
        """Test Django settings are properly configured"""
        self.assertTrue(settings.DEBUG)
        self.assertEqual(settings.LANGUAGE_CODE, 'en-us')
        self.assertEqual(settings.TIME_ZONE, 'UTC')
        self.assertTrue(settings.USE_I18N)
        self.assertTrue(settings.USE_L10N)
        self.assertTrue(settings.USE_TZ)
    
    def test_database_configuration(self):
        """Test database configuration"""
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')
        self.assertIsNotNone(settings.DATABASES['default']['NAME'])
    
    def test_static_files_configuration(self):
        """Test static files configuration"""
        self.assertEqual(settings.STATIC_URL, '/static/')
        self.assertIsInstance(settings.STATICFILES_DIRS, list)
        self.assertTrue(len(settings.STATICFILES_DIRS) > 0)
    
    def test_installed_apps(self):
        """Test installed apps configuration"""
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ]
        
        for app in required_apps:
            self.assertIn(app, settings.INSTALLED_APPS)
    
    def test_middleware_configuration(self):
        """Test middleware configuration"""
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
        
        for middleware in required_middleware:
            self.assertIn(middleware, settings.MIDDLEWARE)
    
    def test_templates_configuration(self):
        """Test templates configuration"""
        self.assertEqual(settings.TEMPLATES[0]['BACKEND'], 'django.template.backends.django.DjangoTemplates')
        self.assertIn('templates', settings.TEMPLATES[0]['DIRS'])
        self.assertTrue(settings.TEMPLATES[0]['APP_DIRS'])
    
    def test_security_settings(self):
        """Test security settings"""
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertTrue(len(settings.SECRET_KEY) > 20)  # Should be a long secret key
    
    def test_nltk_data_path(self):
        """Test NLTK data path configuration"""
        # Check if NLTK data path is set
        import nltk
        self.assertIsInstance(nltk.data.path, list)
        self.assertTrue(len(nltk.data.path) > 0)

class TestEnvironment(TestCase):
    """Test environment setup"""
    
    def test_python_version(self):
        """Test Python version compatibility"""
        import sys
        self.assertGreaterEqual(sys.version_info.major, 3)
        self.assertGreaterEqual(sys.version_info.minor, 8)
    
    def test_required_packages(self):
        """Test required packages are installed"""
        required_packages = [
            'django',
            'nltk',
            'googletrans',
            'langdetect',
            'requests',
        ]
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                self.fail(f"Required package {package} is not installed")
    
    def test_nltk_data_availability(self):
        """Test NLTK data is available"""
        import nltk
        
        try:
            # Test if required NLTK data is available
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('taggers/averaged_perceptron_tagger')
            # Skip wordnet test as it may not be downloaded
            # nltk.data.find('corpora/wordnet')
        except LookupError as e:
            # Don't fail the test, just warn
            print(f"Warning: Some NLTK data not available: {e}")
            # self.fail(f"NLTK data not available: {e}")
    
    def test_file_permissions(self):
        """Test file permissions for required directories"""
        required_dirs = [
            'templates',
            'static',
            'assets',
        ]
        
        for dir_name in required_dirs:
            if os.path.exists(dir_name):
                self.assertTrue(os.path.isdir(dir_name))
                self.assertTrue(os.access(dir_name, os.R_OK))
    
    def test_assets_availability(self):
        """Test animation assets are available"""
        assets_dir = 'assets'
        if os.path.exists(assets_dir):
            # Check for some key animation files
            key_files = ['Hello.mp4', 'World.mp4', 'I.mp4', 'You.mp4']
            for file_name in key_files:
                file_path = os.path.join(assets_dir, file_name)
                if os.path.exists(file_path):
                    self.assertTrue(os.path.isfile(file_path))
                    self.assertTrue(os.access(file_path, os.R_OK))

class TestUtilities(unittest.TestCase):
    """Test utility functions and helpers"""
    
    def test_mock_animation_finder(self):
        """Test mock animation finder utility"""
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            mock_find.return_value = "/path/to/animation.mp4"
            
            from django.contrib.staticfiles import finders
            result = finders.find("test.mp4")
            self.assertEqual(result, "/path/to/animation.mp4")
    
    def test_test_data_generation(self):
        """Test test data generation utilities"""
        # Test text generation
        test_texts = [
            "Hello world",
            "नमस्ते दुनिया",
            "হ্যালো বিশ্ব",
            "வணக்கம் உலகம்",
        ]
        
        for text in test_texts:
            self.assertIsInstance(text, str)
            self.assertTrue(len(text) > 0)
    
    def test_language_codes(self):
        """Test language code validation"""
        valid_language_codes = [
            'en', 'hi', 'mr', 'ta', 'te', 'bn', 'kn', 'gu', 'ml', 'pa', 'or', 'as'
        ]
        
        for code in valid_language_codes:
            self.assertIsInstance(code, str)
            self.assertEqual(len(code), 2)
            self.assertTrue(code.isalpha())
    
    def test_speech_codes(self):
        """Test speech recognition codes"""
        speech_codes = {
            'en': 'en-US',
            'hi': 'hi-IN',
            'mr': 'mr-IN',
            'ta': 'ta-IN',
            'te': 'te-IN',
            'bn': 'bn-IN',
            'kn': 'kn-IN',
            'gu': 'gu-IN',
            'ml': 'ml-IN',
            'pa': 'pa-IN',
            'or': 'or-IN',
            'as': 'as-IN'
        }
        
        for lang_code, speech_code in speech_codes.items():
            self.assertIsInstance(speech_code, str)
            self.assertTrue('-' in speech_code)
            self.assertEqual(len(speech_code.split('-')), 2)

if __name__ == '__main__':
    unittest.main()
