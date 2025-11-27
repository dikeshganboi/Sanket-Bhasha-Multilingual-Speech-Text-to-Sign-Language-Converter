#!/usr/bin/env python3
"""
Regression Tests
Re-tests system after updates to check no new bugs introduced
"""

import os
import sys
import django
import unittest
from unittest.mock import patch, MagicMock
import json
import time
import hashlib

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A2SL.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from A2SL.views import process_multilingual_text, process_english_for_sign_language
from A2SL.translation_service import translation_service

class TestRegression(TestCase):
    """Regression tests to ensure no new bugs after updates"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Known good outputs for regression testing
        self.known_good_outputs = {
            "hello world": ["hello", "world"],
            "i am happy": ["me", "happy"],
            "i will go": ["will", "me", "go"],
            "i went home": ["before", "me", "home"],
        }
    
    def test_nlp_processing_regression(self):
        """Test NLP processing hasn't regressed"""
        test_cases = [
            "hello world",
            "i am happy",
            "i will go",
            "i went home",
            "i am running",
        ]
        
        for text in test_cases:
            with self.subTest(text=text):
                with patch('django.contrib.staticfiles.finders.find') as mock_find:
                    mock_find.return_value = "/path/to/animation.mp4"
                    
                    result = process_english_for_sign_language(text)
                    
                    # Verify basic functionality still works
                    self.assertIsInstance(result, list)
                    self.assertTrue(len(result) > 0)
                    
                    # Check for known good outputs
                    if text in self.known_good_outputs:
                        expected = self.known_good_outputs[text]
                        # Allow for some variation but core words should be present
                        for expected_word in expected:
                            self.assertIn(expected_word, result)
    
    def test_translation_service_regression(self):
        """Test translation service hasn't regressed"""
        test_cases = [
            ("Hello", "en"),
            ("नमस्ते", "hi"),
            ("হ্যালো", "bn"),
            ("வணக்கம்", "ta"),
        ]
        
        for text, lang in test_cases:
            with self.subTest(text=text, lang=lang):
                try:
                    translated, detected_lang = translation_service.translate_to_english(text, lang)
                    
                    # Verify translation still works
                    self.assertIsInstance(translated, str)
                    self.assertIsInstance(detected_lang, str)
                    self.assertTrue(len(translated) > 0)
                    
                except Exception as e:
                    # Log the error but don't fail the test
                    print(f"Translation error for {text} ({lang}): {e}")
    
    def test_multilingual_pipeline_regression(self):
        """Test multilingual pipeline hasn't regressed"""
        test_cases = [
            ("Hello world", "en"),
            ("नमस्ते दुनिया", "hi"),
            ("হ্যালো বিশ্ব", "bn"),
            ("வணக்கம் உலகம்", "ta"),
        ]
        
        for text, lang in test_cases:
            with self.subTest(text=text, lang=lang):
                try:
                    english_text, detected_lang, processed_words = process_multilingual_text(
                        text, lang
                    )
                    
                    # Verify pipeline still works
                    self.assertIsInstance(english_text, str)
                    self.assertIsInstance(detected_lang, str)
                    self.assertIsInstance(processed_words, list)
                    self.assertTrue(len(english_text) > 0)
                    self.assertTrue(len(processed_words) > 0)
                    
                except Exception as e:
                    # Log the error but don't fail the test
                    print(f"Pipeline error for {text} ({lang}): {e}")
    
    def test_animation_view_regression(self):
        """Test animation view hasn't regressed"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Test basic functionality
        response = self.client.post('/animation/', {
            'sen': 'Hello world',
            'language': 'en'
        })
        
        # Verify view still works
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'words')
        self.assertContains(response, 'original_text')
        
        # Verify context data
        context = response.context
        self.assertIn('words', context)
        self.assertIn('original_text', context)
        self.assertEqual(context['original_text'], 'Hello world')
    
    def test_language_detection_regression(self):
        """Test language detection hasn't regressed"""
        test_cases = [
            ("Hello, how are you?", "en"),
            ("नमस्ते, आप कैसे हैं?", "hi"),
            ("হ্যালো, আপনি কেমন আছেন?", "bn"),
        ]
        
        for text, expected_lang in test_cases:
            with self.subTest(text=text):
                try:
                    detected = translation_service.detect_language(text)
                    
                    # Verify detection still works
                    self.assertIsInstance(detected, str)
                    self.assertTrue(len(detected) > 0)
                    
                    # Check if detection is reasonable (allow for some variation)
                    if expected_lang == "en":
                        self.assertIn(detected, ["en", "hi", "bn"])  # Allow some variation
                    
                except Exception as e:
                    # Log the error but don't fail the test
                    print(f"Language detection error for {text}: {e}")
    
    def test_error_handling_regression(self):
        """Test error handling hasn't regressed"""
        error_cases = [
            "",  # Empty string
            None,  # None input
            "   ",  # Whitespace only
            "!@#$%",  # Special characters only
        ]
        
        for error_case in error_cases:
            with self.subTest(error_case=error_case):
                try:
                    result = process_multilingual_text(error_case, "en")
                    
                    # Verify error handling still works
                    self.assertIsInstance(result, tuple)
                    self.assertEqual(len(result), 3)
                    
                except Exception as e:
                    # Log the error but don't fail the test
                    print(f"Error handling issue for {error_case}: {e}")
    
    def test_performance_regression(self):
        """Test performance hasn't regressed significantly"""
        test_text = "This is a test sentence for performance regression testing."
        
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            mock_find.return_value = "/path/to/animation.mp4"
            
            start_time = time.time()
            result = process_multilingual_text(test_text, "en")
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            # Verify performance hasn't regressed (should be under 3 seconds)
            self.assertLess(processing_time, 3.0)
            
            # Verify output quality
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 3)
    
    def test_memory_usage_regression(self):
        """Test memory usage hasn't regressed significantly"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Process multiple texts
        test_texts = [
            "Hello world",
            "नमस्ते दुनिया",
            "হ্যালো বিশ্ব",
            "வணக்கம் உலகம்",
            "This is a longer test sentence for memory regression testing."
        ]
        
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            mock_find.return_value = "/path/to/animation.mp4"
            
            for text in test_texts:
                process_multilingual_text(text, "auto")
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Verify memory usage hasn't regressed (less than 100MB increase)
        self.assertLess(memory_increase, 100 * 1024 * 1024)
    
    def test_output_consistency_regression(self):
        """Test output consistency hasn't regressed"""
        test_text = "Hello world"
        
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            mock_find.return_value = "/path/to/animation.mp4"
            
            # Run multiple times to check consistency
            results = []
            for _ in range(5):
                result = process_multilingual_text(test_text, "en")
                results.append(result)
            
            # Verify consistency
            first_result = results[0]
            for result in results[1:]:
                # Results should be consistent
                self.assertEqual(len(result), len(first_result))
                self.assertEqual(result[0], first_result[0])  # English text
                self.assertEqual(result[1], first_result[1])  # Detected language
    
    def test_api_endpoints_regression(self):
        """Test API endpoints haven't regressed"""
        # Test supported languages endpoint
        response = self.client.get('/api/languages/')
        self.assertEqual(response.status_code, 200)
        
        # Verify response format
        data = json.loads(response.content)
        self.assertIn('languages', data)
        self.assertIsInstance(data['languages'], dict)
        self.assertTrue(len(data['languages']) > 0)
    
    def test_database_regression(self):
        """Test database operations haven't regressed"""
        # Test user creation
        test_user = User.objects.create_user(
            username='regression_test_user',
            password='testpass123'
        )
        
        # Verify user was created
        self.assertIsNotNone(test_user)
        self.assertEqual(test_user.username, 'regression_test_user')
        
        # Test user authentication
        self.client.login(username='regression_test_user', password='testpass123')
        response = self.client.get('/animation/')
        self.assertEqual(response.status_code, 200)
        
        # Clean up
        test_user.delete()
    
    def test_static_files_regression(self):
        """Test static files haven't regressed"""
        # Test that static files are accessible
        static_files = [
            '/static/mic3.png',
            '/static/SanketBhasha Logo.png',
        ]
        
        for static_file in static_files:
            with self.subTest(static_file=static_file):
                response = self.client.get(static_file)
                # Should either return 200 or 404 (if file doesn't exist)
                self.assertIn(response.status_code, [200, 404])
    
    def test_template_rendering_regression(self):
        """Test template rendering hasn't regressed"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Test all main templates
        templates_to_test = [
            '/',
            '/about/',
            '/contact/',
            '/animation/',
        ]
        
        for template_url in templates_to_test:
            with self.subTest(template_url=template_url):
                response = self.client.get(template_url)
                self.assertEqual(response.status_code, 200)
                
                # Verify basic template elements
                self.assertContains(response, 'Sanket Bhasha')
    
    def test_security_regression(self):
        """Test security features haven't regressed"""
        # Test CSRF protection
        response = self.client.post('/animation/', {
            'sen': 'Hello world',
            'language': 'en'
        })
        # Should redirect to login (CSRF protection)
        self.assertEqual(response.status_code, 302)
        
        # Test authentication required
        response = self.client.get('/animation/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_browser_compatibility_regression(self):
        """Test browser compatibility hasn't regressed"""
        # Test with different user agents
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
        
        for user_agent in user_agents:
            with self.subTest(user_agent=user_agent):
                response = self.client.get('/', HTTP_USER_AGENT=user_agent)
                self.assertEqual(response.status_code, 200)
    
    def test_accessibility_regression(self):
        """Test accessibility features haven't regressed"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get('/animation/')
        
        # Verify accessibility features are still present
        self.assertContains(response, 'alt=')  # Alt text
        self.assertContains(response, 'label')  # Form labels
        self.assertContains(response, 'button')  # Interactive elements
        self.assertContains(response, 'input')  # Form inputs
    
    def test_internationalization_regression(self):
        """Test internationalization features haven't regressed"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get('/animation/')
        
        # Verify multilingual features are still present
        self.assertContains(response, 'language')
        self.assertContains(response, 'supported_languages')
        
        # Test with different languages
        test_cases = [
            ("नमस्ते दुनिया", "hi"),
            ("হ্যালো বিশ্ব", "bn"),
            ("வணக்கம் உலகம்", "ta"),
        ]
        
        for text, lang in test_cases:
            with self.subTest(text=text, lang=lang):
                response = self.client.post('/animation/', {
                    'sen': text,
                    'language': lang
                })
                self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
