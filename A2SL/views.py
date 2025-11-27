from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from .translation_service import translation_service
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from typing import Tuple

def home_view(request):
	return render(request,'home.html')


def about_view(request):
	return render(request,'about.html')


def contact_view(request):
	return render(request,'contact.html')

# API endpoint to get supported languages
@require_http_methods(["GET"])
def get_supported_languages(request):
    """Return list of supported languages for frontend"""
    languages = translation_service.get_supported_languages()
    # Filter to only show currently active languages (English and Hindi)
    active_languages = {
        code: info for code, info in languages.items() 
        if info.get('active', False)
    }
    return JsonResponse({'languages': active_languages})

# Process multilingual text for sign language conversion
def process_multilingual_text(text: str, selected_language: str = 'auto') -> Tuple[str, str, list]:
    """
    Process text in any supported language and convert to English for sign language.
    This function now includes:
    - Preprocessing of text before translation.
    - Auto-detection of language if not specified.
    - Translation to English using the translation service.
    - Post-processing to enhance translation quality.
    - Conversion of the final English text to sign language words.
    """
    logger = logging.getLogger(__name__)

    try:
        if not text or not text.strip():
            return "", "en", []

        # Auto-detect language if needed
        if selected_language == 'auto':
            detected_language = translation_service.detect_language(text)
            if not translation_service.is_language_supported(detected_language):
                logger.warning(f"Detected language '{detected_language}' is not supported. Defaulting to English.")
                detected_language = 'en'
        else:
            detected_language = selected_language

        # Preprocess text before translation
        preprocessed_text = translation_service.preprocess_text_for_translation(text, detected_language)

        # Translate to English if the source language is not English
        if detected_language != 'en':
            english_text, _ = translation_service.translate_to_english(preprocessed_text, detected_language)
            
            # Validate translation quality
            if not translation_service.validate_translation_quality(preprocessed_text, english_text, detected_language):
                logger.warning(f"Poor translation quality detected, using alternative translation")
                english_text = translation_service.get_alternative_translation(preprocessed_text, detected_language)
            
            # Enhance the quality of the translation for better sign language conversion
            english_text = translation_service.enhance_translation_quality(preprocessed_text, english_text, detected_language)
        else:
            english_text = preprocessed_text

        logger.info(f"Original ('{detected_language}'): '{text}' -> Preprocessed: '{preprocessed_text}' -> English: '{english_text}'")

        # Process the final English text to get sign language words
        processed_words = process_english_for_sign_language(english_text)

        return english_text, detected_language, processed_words

    except Exception as e:
        logger.error(f"Multilingual text processing failed: {e}")
        # Fallback to basic processing of original text
        processed_words = process_english_for_sign_language(text)
        return text, 'en', processed_words

def process_english_for_sign_language(text):
    """
    Process English text for sign language conversion (extracted from original logic)
    """
    if not text:
        return []
    
    # Tokenizing the sentence and removing punctuation
    text = text.lower()
    words = word_tokenize(text)
    
    # Remove punctuation tokens
    words = [word for word in words if word.isalpha()]
    
    tagged = nltk.pos_tag(words)
    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
    tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])
    
    # Stopwords that will be removed
    stop_words = set(["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])
    
    # Removing stopwords, punctuation, and applying lemmatizing nlp process to words
    lr = WordNetLemmatizer()
    filtered_text = []
    for w,p in zip(words,tagged):
        # Skip punctuation and stopwords
        if w not in stop_words and w.isalpha():  # Only keep alphabetic words
            if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
                filtered_text.append(lr.lemmatize(w,pos='v'))
            elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
                filtered_text.append(lr.lemmatize(w,pos='a'))
            else:
                filtered_text.append(lr.lemmatize(w))
    
    # Adding the specific word to specify tense
    words = filtered_text
    temp=[]
    for w in words:
        if w=='I':
            temp.append('Me')
        else:
            temp.append(w)
    words = temp
    probable_tense = max(tense,key=tense.get)
    
    if probable_tense == "past" and tense["past"]>=1:
        temp = ["Before"]
        temp = temp + words
        words = temp
    elif probable_tense == "future" and tense["future"]>=1:
        if "Will" not in words:
                temp = ["Will"]
                temp = temp + words
                words = temp
        else:
            pass
    elif probable_tense == "present":
        if tense["present_continuous"]>=1:
            temp = ["Now"]
            temp = temp + words
            words = temp
    
    filtered_text = []
    for w in words:
        path = w + ".mp4"
        f = finders.find(path)
        # Splitting the word if its animation is not present in database
        if not f:
            for c in w:
                filtered_text.append(c)
        # Otherwise animation of word
        else:
            filtered_text.append(w)
    
    return filtered_text

@login_required(login_url="login")
def animation_view(request):
    if request.method == 'POST':
        # Get input data
        original_text = request.POST.get('sen', '').strip()
        selected_language = request.POST.get('language', 'en')
        
        if not original_text:
            return render(request, 'animation.html', {
                'error': 'Please enter some text or use the microphone.',
                'supported_languages': translation_service.get_supported_languages()
            })
        
        # Process multilingual text
        english_text, detected_language, processed_words = process_multilingual_text(
            original_text, selected_language
        )
        
        # Get language information
        source_lang_info = translation_service.get_language_info(detected_language)
        
        context = {
            'words': processed_words,
            'original_text': original_text,
            'english_text': english_text,
            'detected_language': detected_language,
            'source_language_name': source_lang_info.get('native_name', source_lang_info.get('name')),
            'selected_language': selected_language,
            'supported_languages': translation_service.get_supported_languages(),
            'translation_performed': detected_language != 'en'
        }
        
        return render(request, 'animation.html', context)
    else:
        # GET request - show the form with language options
        context = {
            'supported_languages': translation_service.get_supported_languages()
        }
        return render(request, 'animation.html', context)




def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request,user)
			# log the user in
			return redirect('animation')
	else:
		form = UserCreationForm()
	return render(request,'signup.html',{'form':form})



def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			#log in user
			user = form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('animation')
	else:
		form = AuthenticationForm()
	return render(request,'login.html',{'form':form})


def logout_view(request):
	logout(request)
	return redirect("home")
