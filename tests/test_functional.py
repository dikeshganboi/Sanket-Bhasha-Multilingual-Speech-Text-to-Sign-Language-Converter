#!/usr/bin/env python3
"""
Functional Tests
Tests user interactions: text input → avatar output, voice input → avatar output
"""

import os
import sys
import django
import unittest
from unittest.mock import patch, MagicMock
import json
import time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A2SL.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from A2SL.views import animation_view, process_multilingual_text

class TestFunctional(TestCase):
    """Functional tests for user interactions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_text_input_to_avatar_output(self):
        """Test complete text input to avatar output flow"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Test English text input
        response = self.client.post('/animation/', {
            'sen': 'Hello world',
            'language': 'en'
        })
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'words')
        self.assertContains(response, 'original_text')
        self.assertContains(response, 'Hello world')
        
        # Verify context data
        context = response.context
        self.assertIn('words', context)
        self.assertIn('original_text', context)
        self.assertEqual(context['original_text'], 'Hello world')
        self.assertIsInstance(context['words'], list)
        self.assertTrue(len(context['words']) > 0)
    
    def test_voice_input_simulation(self):
        """Test voice input simulation (mocked speech recognition)"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Simulate voice input
        voice_text = "Hello, how are you today?"
        
        response = self.client.post('/animation/', {
            'sen': voice_text,
            'language': 'en'
        })
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, voice_text)
        self.assertContains(response, 'words')
        
        # Verify processing
        context = response.context
        self.assertIsInstance(context['words'], list)
        self.assertTrue(len(context['words']) > 0)
    
    def test_multilingual_text_input(self):
        """Test multilingual text input functionality"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        test_cases = [
            ("नमस्ते दुनिया", "hi"),
            ("হ্যালো বিশ্ব", "bn"),
            ("வணக்கம் உலகம்", "ta"),
            ("Hello world", "en"),
        ]
        
        for text, lang in test_cases:
            with self.subTest(text=text, lang=lang):
                response = self.client.post('/animation/', {
                    'sen': text,
                    'language': lang
                })
                
                # Verify response
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, text)
                self.assertContains(response, 'words')
                
                # Verify context
                context = response.context
                self.assertIn('original_text', context)
                self.assertIn('words', context)
                self.assertEqual(context['original_text'], text)
                self.assertIsInstance(context['words'], list)
    
    def test_language_selection_functionality(self):
        """Test language selection dropdown functionality"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Test GET request (form display)
        response = self.client.get('/animation/')
        
        # Verify form is displayed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'language')
        self.assertContains(response, 'supported_languages')
        
        # Verify language options are available
        context = response.context
        self.assertIn('supported_languages', context)
        self.assertIsInstance(context['supported_languages'], dict)
        self.assertTrue(len(context['supported_languages']) > 0)
    
    def test_auto_language_detection(self):
        """Test automatic language detection functionality"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        test_cases = [
            ("Hello world", "auto"),
            ("नमस्ते दुनिया", "auto"),
            ("হ্যালো বিশ্ব", "auto"),
        ]
        
        for text, lang in test_cases:
            with self.subTest(text=text, lang=lang):
                response = self.client.post('/animation/', {
                    'sen': text,
                    'language': lang
                })
                
                # Verify response
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, text)
                
                # Verify language detection
                context = response.context
                self.assertIn('detected_language', context)
                self.assertIsInstance(context['detected_language'], str)
    
    def test_error_handling_functional(self):
        """Test error handling in user interactions"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Test empty input
        response = self.client.post('/animation/', {
            'sen': '',
            'language': 'en'
        })
        
        # Verify error handling
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')
        
        # Test whitespace-only input
        response = self.client.post('/animation/', {
            'sen': '   ',
            'language': 'en'
        })
        
        # Verify error handling
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')
    
    def test_animation_playback_functionality(self):
        """Test animation playback functionality"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Test with text that should generate animations
        response = self.client.post('/animation/', {
            'sen': 'Hello world',
            'language': 'en'
        })
        
        # Verify animation-related content
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'videoPlayer')
        self.assertContains(response, 'playPause')
        
        # Verify words are generated for animation
        context = response.context
        self.assertIn('words', context)
        self.assertIsInstance(context['words'], list)
        self.assertTrue(len(context['words']) > 0)
    
    def test_user_authentication_flow(self):
        """Test user authentication flow"""
        # Test unauthenticated access
        response = self.client.get('/animation/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test login
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        
        # Test authenticated access
        response = self.client.get('/animation/')
        self.assertEqual(response.status_code, 200)
    
    def test_session_management(self):
        """Test session management functionality"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Test session persistence
        response1 = self.client.get('/animation/')
        self.assertEqual(response1.status_code, 200)
        
        response2 = self.client.get('/animation/')
        self.assertEqual(response2.status_code, 200)
        
        # Verify session is maintained
        self.assertTrue(response1.wsgi_request.user.is_authenticated)
        self.assertTrue(response2.wsgi_request.user.is_authenticated)
    
    def test_responsive_design_functionality(self):
        """Test responsive design functionality"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Test with different user agents (simulated)
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
            'Mozilla/5.0 (Android 10; Mobile; rv:68.0) Gecko/68.0',
        ]
        
        for user_agent in user_agents:
            with self.subTest(user_agent=user_agent):
                response = self.client.get('/animation/', HTTP_USER_AGENT=user_agent)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'animation')
    
    def test_performance_functional(self):
        """Test performance of user interactions"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Test response time
        start_time = time.time()
        response = self.client.post('/animation/', {
            'sen': 'Hello world',
            'language': 'en'
        })
        end_time = time.time()
        
        # Verify performance
        self.assertEqual(response.status_code, 200)
        response_time = end_time - start_time
        self.assertLess(response_time, 3.0)  # Should respond within 3 seconds
    
    def test_concurrent_user_sessions(self):
        """Test concurrent user sessions"""
        import threading
        import time
        
        results = []
        errors = []
        
        def user_session(user_id):
            try:
                # Create separate client for each user
                client = Client()
                user = User.objects.create_user(
                    username=f'testuser{user_id}',
                    password='testpass123'
                )
                
                # Login and test
                client.login(username=f'testuser{user_id}', password='testpass123')
                response = client.post('/animation/', {
                    'sen': f'Hello from user {user_id}',
                    'language': 'en'
                })
                
                results.append(response.status_code)
            except Exception as e:
                errors.append(e)
        
        # Create multiple concurrent sessions
        threads = []
        for i in range(5):
            thread = threading.Thread(target=user_session, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify concurrent sessions
        self.assertEqual(len(results), 5)
        self.assertEqual(len(errors), 0)
        self.assertTrue(all(status == 200 for status in results))
    
    def test_data_persistence_functional(self):
        """Test data persistence across requests"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # First request
        response1 = self.client.post('/animation/', {
            'sen': 'Hello world',
            'language': 'en'
        })
        
        # Second request
        response2 = self.client.post('/animation/', {
            'sen': 'Goodbye world',
            'language': 'en'
        })
        
        # Verify both requests work independently
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
        # Verify context data is correct for each request
        context1 = response1.context
        context2 = response2.context
        
        self.assertEqual(context1['original_text'], 'Hello world')
        self.assertEqual(context2['original_text'], 'Goodbye world')
    
    def test_accessibility_functionality(self):
        """Test accessibility features"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get('/animation/')
        
        # Verify accessibility features
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alt=')  # Alt text for images
        self.assertContains(response, 'label')  # Form labels
        self.assertContains(response, 'button')  # Interactive elements

if __name__ == '__main__':
    unittest.main()
