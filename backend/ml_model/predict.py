"""
Prediction Module for Expense Classification
"""
import torch
import re
import numpy as np
from .load_model import get_loaded_model


def preprocess_sms_text(text):
    """
    Preprocess SMS text for model input
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep rupee symbol and numbers
    text = re.sub(r'[^\w\s₹rs.,-]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def text_to_sequence(text, vectorizer=None, max_length=100):
    """
    Convert text to sequence of integers
    This is a simple tokenizer - in production, use the trained vectorizer
    """
    if vectorizer is not None:
        # Use trained vectorizer
        return vectorizer.transform([text])
    
    # Simple word-level tokenization (fallback)
    words = text.split()
    
    # Create a simple vocabulary (this should match training)
    # In production, load the actual vocabulary from training
    vocab = {word: idx + 1 for idx, word in enumerate(set(words))}
    
    # Convert to sequence
    sequence = [vocab.get(word, 0) for word in words[:max_length]]
    
    # Pad sequence
    if len(sequence) < max_length:
        sequence = sequence + [0] * (max_length - len(sequence))
    
    return np.array([sequence])


def predict_category(sms_text: str) -> dict:
    """
    Predict expense category from SMS text
    
    Args:
        sms_text (str): Raw SMS text
    
    Returns:
        dict: {
            'category': predicted category name,
            'confidence': confidence score (0-1),
            'all_probabilities': dict of all categories with probabilities
        }
    """
    try:
        # Load model
        model, vectorizer, label_encoder = get_loaded_model()
        
        if model is None:
            return {
                'category': 'other',
                'confidence': 0.0,
                'error': 'Model not loaded'
            }
        
        # Preprocess text
        processed_text = preprocess_sms_text(sms_text)
        
        if not processed_text:
            return {
                'category': 'other',
                'confidence': 0.0,
                'error': 'Empty text after preprocessing'
            }
        
        # Convert to sequence
        sequence = text_to_sequence(processed_text, vectorizer)
        
        # Convert to tensor
        input_tensor = torch.LongTensor(sequence)
        
        # Get prediction
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, dim=1)
            
            predicted_idx = predicted_idx.item()
            confidence = confidence.item()
        
        # Get category name
        category = label_encoder.get(predicted_idx, 'other')
        
        # Get all probabilities
        all_probs = {}
        for idx, prob in enumerate(probabilities[0].tolist()):
            cat_name = label_encoder.get(idx, f'category_{idx}')
            all_probs[cat_name] = round(prob, 4)
        
        return {
            'category': category,
            'confidence': round(confidence, 4),
            'all_probabilities': all_probs,
            'preprocessed_text': processed_text
        }
    
    except Exception as e:
        return {
            'category': 'other',
            'confidence': 0.0,
            'error': str(e)
        }


def predict_category_batch(sms_texts: list) -> list:
    """
    Predict categories for multiple SMS texts
    
    Args:
        sms_texts (list): List of SMS texts
    
    Returns:
        list: List of prediction dictionaries
    """
    return [predict_category(text) for text in sms_texts]
