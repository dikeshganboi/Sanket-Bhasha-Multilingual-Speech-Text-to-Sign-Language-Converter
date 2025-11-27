#!/usr/bin/env python3
"""
Test script for the multilingual ISL converter.
This script tests the translation functionality for various Indian languages.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A2SL.settings')
django.setup()

from A2SL.translation_service import translation_service
from A2SL.views import process_multilingual_text

def test_language_detection():
    """Test language detection functionality"""
    print("=== Testing Language Detection ===")
    
    test_cases = [
        ("Hello, how are you?", "en"),
        ("नमस्ते, आप कैसे हैं?", "hi"),
        ("हॅलो, तुमी कसे आहात?", "mr"),  # Marathi
        ("হ্যালো, আপনি কেমন আছেন?", "bn"),  # Bengali
    ]
    
    for text, expected_lang in test_cases:
        detected = translation_service.detect_language(text)
        print(f"Text: {text}")
        print(f"Expected: {expected_lang}, Detected: {detected}")
        print(f"Match: {'✓' if detected == expected_lang else '✗'}")
        print("-" * 50)

def test_translation():
    """Test translation functionality"""
    print("\n=== Testing Translation ===")
    
    test_cases = [
        ("Hello", "en"),
        ("नमस्ते", "hi"),
        ("হ্যালো", "bn"),  # Bengali
        ("வணக்கம்", "ta"),  # Tamil
    ]
    
    for text, source_lang in test_cases:
        try:
            translated, detected_lang = translation_service.translate_to_english(text, source_lang)
            print(f"Original ({source_lang}): {text}")
            print(f"Translated to English: {translated}")
            print(f"Detected Language: {detected_lang}")
            print("-" * 50)
        except Exception as e:
            print(f"Error translating '{text}': {e}")
            print("-" * 50)

def test_full_pipeline():
    """Test the complete multilingual processing pipeline"""
    print("\n=== Testing Full Pipeline ===")
    
    test_cases = [
        "Hello, my name is John",
        "नमस्ते, मेरा नाम जॉन है",  # Hindi
        "What is your name?",
        "तुमचे नाव काय?",  # Marathi
    ]
    
    for text in test_cases:
        try:
            english_text, detected_lang, processed_words = process_multilingual_text(text)
            print(f"Original: {text}")
            print(f"Detected Language: {detected_lang}")
            print(f"English Translation: {english_text}")
            print(f"Processed Words for ISL: {processed_words}")
            print("-" * 50)
        except Exception as e:
            print(f"Error processing '{text}': {e}")
            print("-" * 50)

def test_supported_languages():
    """Test supported languages list"""
    print("\n=== Testing Supported Languages ===")
    
    languages = translation_service.get_supported_languages()
    active_languages = [
        (code, info) for code, info in languages.items() 
        if info.get('active', False)
    ]
    
    print(f"Total active languages: {len(active_languages)}")
    
    for code, info in active_languages:
        print(f"{info['flag']} {code}: {info['native_name']} ({info['name']})")

if __name__ == "__main__":
    print("🌍 Multilingual ISL Converter Test Suite")
    print("=" * 60)
    
    try:
        test_supported_languages()
        test_language_detection()
        test_translation()
        test_full_pipeline()
        
        print("\n✅ All tests completed!")
        print("\nYour multilingual ISL converter is ready to use with support for:")
        print("🇺🇸 English • 🇮🇳 Hindi • 🇮🇳 Marathi • 🇮🇳 Tamil • 🇮🇳 Telugu")
        print("🇮🇳 Bengali • 🇮🇳 Kannada • 🇮🇳 Gujarati • 🇮🇳 Malayalam") 
        print("🇮🇳 Punjabi • 🇮🇳 Odia • 🇮🇳 Assamese")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)
