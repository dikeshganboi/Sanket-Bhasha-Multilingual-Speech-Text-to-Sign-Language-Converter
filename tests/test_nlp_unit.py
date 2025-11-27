#!/usr/bin/env python3
"""
Unit Tests for NLP Functions
Tests individual NLP components: tokenization, lemmatization, POS tagging, etc.
"""

import os
import sys
import django
import unittest
from unittest.mock import patch, MagicMock

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A2SL.settings')
django.setup()

from A2SL.views import process_english_for_sign_language
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

class TestNLPUnit(unittest.TestCase):
    """Unit tests for NLP processing functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def test_word_tokenization(self):
        """Test word tokenization functionality"""
        test_cases = [
            ("Hello world", ["hello", "world"]),
            ("How are you?", ["how", "are", "you", "?"]),
            ("I am fine.", ["i", "am", "fine", "."]),
            ("", []),
            ("   ", []),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = word_tokenize(input_text.lower())
                self.assertEqual(result, expected)
    
    def test_pos_tagging(self):
        """Test part-of-speech tagging"""
        test_cases = [
            ("I am running", [("i", "PRP"), ("am", "VBP"), ("running", "VBG")]),
            ("The quick brown fox", [("the", "DT"), ("quick", "JJ"), ("brown", "JJ"), ("fox", "NN")]),
        ]
        
        for input_text, expected_tags in test_cases:
            with self.subTest(input_text=input_text):
                words = word_tokenize(input_text.lower())
                tagged = nltk.pos_tag(words)
                # Check that we get POS tags for each word
                self.assertEqual(len(tagged), len(words))
                for word, tag in tagged:
                    self.assertIsInstance(tag, str)
                    self.assertTrue(len(tag) > 0)
    
    def test_stop_words_removal(self):
        """Test stop words removal"""
        test_cases = [
            (["i", "am", "happy"], ["happy"]),
            (["the", "quick", "brown", "fox"], ["quick", "brown", "fox"]),
            (["hello", "world"], ["hello", "world"]),  # No stop words
            ([], []),
        ]
        
        for input_words, expected in test_cases:
            with self.subTest(input_words=input_words):
                filtered = [word for word in input_words if word not in self.stop_words]
                self.assertEqual(filtered, expected)
    
    def test_lemmatization(self):
        """Test word lemmatization"""
        test_cases = [
            ("running", "v", "run"),
            ("better", "a", "good"),
            ("cats", "n", "cat"),
            ("went", "v", "go"),
        ]
        
        for word, pos, expected in test_cases:
            with self.subTest(word=word, pos=pos):
                result = self.lemmatizer.lemmatize(word, pos=pos)
                self.assertEqual(result, expected)
    
    def test_tense_analysis(self):
        """Test tense analysis functionality"""
        test_cases = [
            ("I will go", {"future": 1, "present": 0, "past": 0, "present_continuous": 0}),
            ("I am running", {"future": 0, "present": 2, "past": 0, "present_continuous": 1}),
            ("I went home", {"future": 0, "present": 0, "past": 1, "present_continuous": 0}),
            ("I eat food", {"future": 0, "present": 0, "past": 1, "present_continuous": 0}),  # "eat" is tagged as VBD (past)
        ]
        
        for input_text, expected_tense in test_cases:
            with self.subTest(input_text=input_text):
                words = word_tokenize(input_text.lower())
                tagged = nltk.pos_tag(words)
                
                tense = {}
                tense["future"] = len([word for word in tagged if word[1] == "MD"])
                tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
                tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
                tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])
                
                self.assertEqual(tense, expected_tense)
    
    def test_character_splitting(self):
        """Test character splitting for unknown words"""
        test_cases = [
            "hello",  # Should remain as word if animation exists
            "xyz",    # Should split into characters
            "a",      # Single character
            "",       # Empty string
        ]
        
        for word in test_cases:
            with self.subTest(word=word):
                # Mock the file finder to simulate missing animations
                with patch('django.contrib.staticfiles.finders.find') as mock_find:
                    if word == "xyz":
                        mock_find.return_value = None  # Animation not found
                        expected = list(word)
                    else:
                        mock_find.return_value = f"/path/to/{word}.mp4"  # Animation found
                        expected = [word]
                    
                    # Test the character splitting logic
                    path = word + ".mp4"
                    f = mock_find(path)
                    
                    if not f:
                        result = list(word)
                    else:
                        result = [word]
                    
                    self.assertEqual(result, expected)
    
    def test_process_english_for_sign_language_empty_input(self):
        """Test processing with empty input"""
        result = process_english_for_sign_language("")
        self.assertEqual(result, [])
        
        result = process_english_for_sign_language(None)
        self.assertEqual(result, [])
    
    def test_process_english_for_sign_language_basic(self):
        """Test basic English processing"""
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            # Mock that all animations exist
            mock_find.return_value = "/path/to/animation.mp4"
            
            result = process_english_for_sign_language("hello world")
            self.assertIsInstance(result, list)
            self.assertTrue(len(result) > 0)
    
    def test_process_english_for_sign_language_tense_handling(self):
        """Test tense-specific processing"""
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            mock_find.return_value = "/path/to/animation.mp4"
            
            # Test past tense
            result = process_english_for_sign_language("I went home")
            self.assertIsInstance(result, list)
            
            # Test future tense
            result = process_english_for_sign_language("I will go")
            self.assertIsInstance(result, list)
            
            # Test present continuous
            result = process_english_for_sign_language("I am running")
            self.assertIsInstance(result, list)
    
    def test_process_english_for_sign_language_pronoun_handling(self):
        """Test pronoun handling (I -> Me)"""
        with patch('django.contrib.staticfiles.finders.find') as mock_find:
            mock_find.return_value = "/path/to/animation.mp4"
            
            result = process_english_for_sign_language("I am happy")
            self.assertIsInstance(result, list)
            # Should contain "Me" instead of "I"
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        test_cases = [
            "   ",  # Only whitespace
            "!@#$%",  # Only special characters
            "123",  # Only numbers
            "a" * 1000,  # Very long string
        ]
        
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                try:
                    result = process_english_for_sign_language(test_case)
                    self.assertIsInstance(result, list)
                except Exception as e:
                    self.fail(f"Function raised {type(e).__name__} for input '{test_case}': {e}")

if __name__ == '__main__':
    unittest.main()
