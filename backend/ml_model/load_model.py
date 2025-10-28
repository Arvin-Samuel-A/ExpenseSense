"""
ML Model Loading Module
Loads the pretrained CNN model for expense classification
"""
import torch
import torch.nn as nn
import os
from pathlib import Path

# Global variable to store the loaded model
_model = None
_vectorizer = None
_label_encoder = None


class ExpenseCNN(nn.Module):
    """
    CNN Model for SMS expense classification
    Architecture: Embedding -> Conv1D -> MaxPool -> FC -> Softmax
    """
    def __init__(self, vocab_size=10000, embedding_dim=128, num_classes=10, max_length=100):
        super(ExpenseCNN, self).__init__()
        
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        
        # Convolutional layers with different kernel sizes
        self.conv1 = nn.Conv1d(embedding_dim, 128, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(128, 128, kernel_size=4, padding=1)
        self.conv3 = nn.Conv1d(128, 128, kernel_size=5, padding=2)
        
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool1d(kernel_size=2)
        self.dropout = nn.Dropout(0.5)
        
        # Calculate FC input size
        fc_input_size = 128 * 3  # 3 conv outputs concatenated
        
        self.fc1 = nn.Linear(fc_input_size, 64)
        self.fc2 = nn.Linear(64, num_classes)
    
    def forward(self, x):
        # x shape: (batch, seq_len)
        x = self.embedding(x)  # (batch, seq_len, embedding_dim)
        x = x.permute(0, 2, 1)  # (batch, embedding_dim, seq_len)
        
        # Apply convolutions
        x1 = self.relu(self.conv1(x))
        x1 = torch.max(x1, dim=2)[0]  # Global max pooling
        
        x2 = self.relu(self.conv2(x))
        x2 = torch.max(x2, dim=2)[0]
        
        x3 = self.relu(self.conv3(x))
        x3 = torch.max(x3, dim=2)[0]
        
        # Concatenate features
        x = torch.cat([x1, x2, x3], dim=1)
        
        x = self.dropout(x)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x


def get_model_path():
    """Get the path to the saved model file"""
    base_dir = Path(__file__).resolve().parent
    model_path = base_dir / 'expense_cnn_model.pt'
    return model_path


def load_expense_model():
    """
    Load the pretrained expense classification model
    Returns: model, vectorizer, label_encoder
    """
    global _model, _vectorizer, _label_encoder
    
    if _model is not None:
        return _model, _vectorizer, _label_encoder
    
    model_path = get_model_path()
    
    if not model_path.exists():
        print(f"Warning: Model file not found at {model_path}")
        print("Creating a dummy model for development. Train the real model for production.")
        
        # Create dummy model for development
        _model = ExpenseCNN()
        _model.eval()
        
        # Dummy vectorizer and label encoder
        _vectorizer = None
        _label_encoder = {
            0: 'food',
            1: 'transport',
            2: 'shopping',
            3: 'entertainment',
            4: 'bills',
            5: 'healthcare',
            6: 'education',
            7: 'groceries',
            8: 'travel',
            9: 'other'
        }
        
        return _model, _vectorizer, _label_encoder
    
    try:
        # Load on CPU (for deployment)
        device = torch.device('cpu')
        checkpoint = torch.load(model_path, map_location=device)
        
        # Extract model components
        model_state = checkpoint.get('model_state_dict', checkpoint)
        _vectorizer = checkpoint.get('vectorizer', None)
        _label_encoder = checkpoint.get('label_encoder', None)
        
        # Initialize model with saved config
        vocab_size = checkpoint.get('vocab_size', 10000)
        embedding_dim = checkpoint.get('embedding_dim', 128)
        num_classes = checkpoint.get('num_classes', 10)
        
        _model = ExpenseCNN(
            vocab_size=vocab_size,
            embedding_dim=embedding_dim,
            num_classes=num_classes
        )
        
        _model.load_state_dict(model_state)
        _model.to(device)
        _model.eval()
        
        print(f"✓ Model loaded from {model_path}")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        # Fallback to dummy model
        _model = ExpenseCNN()
        _model.eval()
        _label_encoder = {i: cat for i, cat in enumerate([
            'food', 'transport', 'shopping', 'entertainment', 'bills',
            'healthcare', 'education', 'groceries', 'travel', 'other'
        ])}
    
    return _model, _vectorizer, _label_encoder


def get_loaded_model():
    """Get the already loaded model (singleton pattern)"""
    global _model, _vectorizer, _label_encoder
    
    if _model is None:
        return load_expense_model()
    
    return _model, _vectorizer, _label_encoder
