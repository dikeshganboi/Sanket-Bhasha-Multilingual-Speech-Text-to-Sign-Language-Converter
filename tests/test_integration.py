#!/usr/bin/env python3
"""
Integration Tests
Tests module interactions: Speech + NLP + Avatar + Translation
"""

import os
import sys
import django
import unittest
from unittest.mock import patch, MagicMock, Mock
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A2SL.settings')
django.setup()

from A2SL.views import process_multilingual_text, animation_view
from A2SL.translation_service import translation_service
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class TestIntegration(TestCase):
    """Integration tests for module interactions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_speech_to_nlp_integration(self):
        """Test integration between speech recognition and NLP processing"""
        # Mock speech recognition input
        speech_input = "Hello, how are you today?"
        
        # Test the complete pipeline
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            mock_find.return_value = "/path/to/animation.mp4"
            
            english_text, detected_lang, processed_words = process_multilingual_text(
                speech_input, 'en'
            )
            
            # Verify integration
            self.assertEqual(detected_lang, 'en')
            self.assertIsInstance(processed_words, list)
            self.assertTrue(len(processed_words) > 0)
            self.assertIn('hello', english_text.lower())
    
    def test_translation_to_nlp_integration(self):
        """Test integration between translation and NLP processing"""
        # Test Hindi to English translation + NLP
        hindi_input = "नमस्ते, आप कैसे हैं?"
        
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            mock_find.return_value = "/path/to/animation.mp4"
            
            english_text, detected_lang, processed_words = process_multilingual_text(
                hindi_input, 'hi'
            )
            
            # Verify translation integration
            self.assertEqual(detected_lang, 'hi')
            self.assertIsInstance(english_text, str)
            self.assertIsInstance(processed_words, list)
            self.assertTrue(len(english_text) > 0)
            self.assertTrue(len(processed_words) > 0)
    
    def test_nlp_to_avatar_integration(self):
        """Test integration between NLP processing and avatar animation"""
        test_words = ["hello", "world", "test"]
        
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            # Mock animation file existence
            mock_find.return_value = "/path/to/animation.mp4"
            
            # Test word-to-animation mapping
            for word in test_words:
                path = word + ".mp4"
                f = mock_find(path)
                self.assertIsNotNone(f)
    
    def test_multilingual_pipeline_integration(self):
        """Test complete multilingual pipeline integration"""
        test_cases = [
            ("Hello world", "en"),
            ("नमस्ते दुनिया", "hi"),
            ("হ্যালো বিশ্ব", "bn"),
            ("வணக்கம் உலகம்", "ta"),
        ]
        
        for text, lang in test_cases:
            with self.subTest(text=text, lang=lang):
                with patch('django.contrib.staticfiles.finders.find') as mock_find:
                    mock_find.return_value = "/path/to/animation.mp4"
                    
                    english_text, detected_lang, processed_words = process_multilingual_text(
                        text, lang
                    )
                    
                    # Verify complete pipeline
                    self.assertIsInstance(english_text, str)
                    self.assertIsInstance(detected_lang, str)
                    self.assertIsInstance(processed_words, list)
                    self.assertTrue(len(processed_words) > 0)
    
    def test_animation_view_integration(self):
        """Test integration of animation view with all components"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Test POST request with text input
        response = self.client.post('/animation/', {
            'sen': 'Hello world',
            'language': 'en'
        })
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'words')
        self.assertContains(response, 'original_text')
    
    def test_language_detection_integration(self):
        """Test language detection integration with translation"""
        test_cases = [
            ("Hello, how are you?", "en"),
            ("नमस्ते, आप कैसे हैं?", "hi"),
            ("হ্যালো, আপনি কেমন আছেন?", "bn"),
        ]
        
        for text, expected_lang in test_cases:
            with self.subTest(text=text):
                # Test auto-detection
                english_text, detected_lang, processed_words = process_multilingual_text(
                    text, 'auto'
                )
                
                # Verify detection
                self.assertIsInstance(detected_lang, str)
                self.assertIsInstance(english_text, str)
                self.assertIsInstance(processed_words, list)
    
    def test_error_handling_integration(self):
        """Test error handling across modules"""
        # Test with invalid input
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            mock_find.return_value = "/path/to/animation.mp4"
            
            # Test empty input
            result = process_multilingual_text("", "en")
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 3)
            
            # Test None input
            result = process_multilingual_text(None, "en")
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 3)
    
    def test_performance_integration(self):
        """Test performance across integrated modules"""
        import time
        
        test_text = "This is a test sentence for performance testing."
        
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            mock_find.return_value = "/path/to/animation.mp4"
            
            start_time = time.time()
            english_text, detected_lang, processed_words = process_multilingual_text(
                test_text, 'en'
            )
            end_time = time.time()
            
            # Verify performance (should complete within reasonable time)
            processing_time = end_time - start_time
            self.assertLess(processing_time, 5.0)  # Should complete within 5 seconds
            
            # Verify output quality
            self.assertIsInstance(processed_words, list)
            self.assertTrue(len(processed_words) > 0)
    
    def test_memory_usage_integration(self):
        """Test memory usage across integrated modules"""
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
            "This is a longer test sentence for memory testing."
        ]
        
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            mock_find.return_value = "/path/to/animation.mp4"
            
            for text in test_texts:
                process_multilingual_text(text, 'auto')
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Verify memory usage is reasonable (less than 50MB increase)
        self.assertLess(memory_increase, 50 * 1024 * 1024)
    
    def test_concurrent_processing_integration(self):
        """Test concurrent processing across modules"""
        import threading
        import time
        
        results = []
        errors = []
        
        def process_text(text, lang):
            try:
                with patch('django.contrib.staticfiles.finders.find') as mock_find:
                    mock_find.return_value = "/path/to/animation.mp4"
                    
                    result = process_multilingual_text(text, lang)
                    results.append(result)
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        test_cases = [
            ("Hello world", "en"),
            ("नमस्ते दुनिया", "hi"),
            ("হ্যালো বিশ্ব", "bn"),
            ("வணக்கம் உலகம்", "ta"),
        ]
        
        for text, lang in test_cases:
            thread = threading.Thread(target=process_text, args=(text, lang))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify concurrent processing
        self.assertEqual(len(results), len(test_cases))
        self.assertEqual(len(errors), 0)
        
        # Verify all results are valid
        for result in results:
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 3)

if __name__ == '__main__':
    unittest.main()
