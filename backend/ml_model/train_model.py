"""
Training Script for Expense CNN Model on Apple Silicon (MPS)

This script trains a CNN model on SMS expense data for category classification.
It uses PyTorch with MPS (Metal Performance Shaders) acceleration for Apple Silicon.

Usage:
    python train_model.py

The trained model will be saved as 'expense_cnn_model.pt'
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from collections import Counter
import re
from pathlib import Path


# Check for MPS (Apple Silicon)
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("✓ Using Apple Silicon MPS acceleration")
elif torch.cuda.is_available():
    device = torch.device("cuda")
    print("✓ Using CUDA")
else:
    device = torch.device("cpu")
    print("✓ Using CPU")


class ExpenseCNN(nn.Module):
    """CNN Model for SMS expense classification"""
    
    def __init__(self, vocab_size=10000, embedding_dim=128, num_classes=10, max_length=100):
        super(ExpenseCNN, self).__init__()
        
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        
        # Multiple conv layers with different kernel sizes
        self.conv1 = nn.Conv1d(embedding_dim, 128, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(128, 128, kernel_size=4, padding=1)
        self.conv3 = nn.Conv1d(128, 128, kernel_size=5, padding=2)
        
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        
        fc_input_size = 128 * 3
        self.fc1 = nn.Linear(fc_input_size, 64)
        self.fc2 = nn.Linear(64, num_classes)
    
    def forward(self, x):
        x = self.embedding(x)
        x = x.permute(0, 2, 1)
        
        x1 = self.relu(self.conv1(x))
        x1 = torch.max(x1, dim=2)[0]
        
        x2 = self.relu(self.conv2(x))
        x2 = torch.max(x2, dim=2)[0]
        
        x3 = self.relu(self.conv3(x))
        x3 = torch.max(x3, dim=2)[0]
        
        x = torch.cat([x1, x2, x3], dim=1)
        x = self.dropout(x)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x


class ExpenseDataset(Dataset):
    """Dataset for expense SMS data"""
    
    def __init__(self, texts, labels, vocab, max_length=100):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        # Convert text to sequence
        sequence = self.text_to_sequence(text)
        
        return torch.LongTensor(sequence), torch.LongTensor([label])
    
    def text_to_sequence(self, text):
        """Convert text to sequence of integers"""
        words = text.split()
        sequence = [self.vocab.get(word, 0) for word in words[:self.max_length]]
        
        # Pad sequence
        if len(sequence) < self.max_length:
            sequence = sequence + [0] * (self.max_length - len(sequence))
        
        return sequence


def preprocess_text(text):
    """Preprocess SMS text"""
    text = text.lower()
    text = re.sub(r'[^\w\s₹rs.,-]', '', text)
    text = ' '.join(text.split())
    return text


def build_vocab(texts, vocab_size=10000):
    """Build vocabulary from texts"""
    word_counts = Counter()
    
    for text in texts:
        words = text.split()
        word_counts.update(words)
    
    # Get most common words
    most_common = word_counts.most_common(vocab_size - 1)
    
    # Create vocab dict (0 is reserved for padding)
    vocab = {word: idx + 1 for idx, (word, _) in enumerate(most_common)}
    
    return vocab


def generate_sample_data():
    """Generate sample training data"""
    
    sample_data = [
        # Food & Dining
        ("Spent Rs 500 at Cafe Coffee Day", "food"),
        ("McDonald's Rs 350 payment successful", "food"),
        ("Swiggy order Rs 450 delivered", "food"),
        ("Zomato payment Rs 600", "food"),
        ("Restaurant bill Rs 800", "food"),
        
        # Transport
        ("Uber ride Rs 150", "transport"),
        ("Ola cab Rs 200 paid", "transport"),
        ("Metro card recharge Rs 500", "transport"),
        ("Petrol Rs 2000", "transport"),
        ("Auto fare Rs 80", "transport"),
        
        # Shopping
        ("Amazon purchase Rs 1500", "shopping"),
        ("Flipkart order Rs 2000", "shopping"),
        ("Myntra shopping Rs 1200", "shopping"),
        ("Payment at store Rs 3000", "shopping"),
        ("Online shopping Rs 1800", "shopping"),
        
        # Entertainment
        ("Movie ticket Rs 300", "entertainment"),
        ("Netflix subscription Rs 649", "entertainment"),
        ("Concert ticket Rs 2000", "entertainment"),
        ("Game purchase Rs 500", "entertainment"),
        ("Amazon Prime Rs 999", "entertainment"),
        
        # Bills
        ("Electricity bill Rs 1500", "bills"),
        ("Water bill Rs 500", "bills"),
        ("Internet bill Rs 999", "bills"),
        ("Mobile recharge Rs 299", "bills"),
        ("Gas cylinder Rs 900", "bills"),
        
        # Groceries
        ("BigBasket order Rs 2500", "groceries"),
        ("Supermarket Rs 1500", "groceries"),
        ("Vegetables Rs 300", "groceries"),
        ("Milk and bread Rs 150", "groceries"),
        ("Monthly groceries Rs 5000", "groceries"),
        
        # Healthcare
        ("Medical store Rs 500", "healthcare"),
        ("Doctor consultation Rs 800", "healthcare"),
        ("Medicine purchase Rs 350", "healthcare"),
        ("Hospital bill Rs 5000", "healthcare"),
        ("Pharmacy Rs 400", "healthcare"),
        
        # Travel
        ("Flight ticket Rs 5000", "travel"),
        ("Hotel booking Rs 3000", "travel"),
        ("Train ticket Rs 800", "travel"),
        ("Bus ticket Rs 500", "travel"),
        ("Trip expenses Rs 10000", "travel"),
    ]
    
    # Duplicate data to have more samples
    sample_data = sample_data * 20
    
    texts = [preprocess_text(text) for text, _ in sample_data]
    labels = [label for _, label in sample_data]
    
    return texts, labels


def train_model(num_epochs=50, batch_size=16, learning_rate=0.001):
    """Train the expense CNN model"""
    
    print("\n=== Training Expense CNN Model ===\n")
    
    # Generate or load data
    print("Loading data...")
    texts, labels = generate_sample_data()
    
    print(f"Total samples: {len(texts)}")
    print(f"Categories: {set(labels)}")
    
    # Encode labels
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)
    label_dict = {idx: label for idx, label in enumerate(label_encoder.classes_)}
    
    print(f"\nLabel mapping: {label_dict}")
    
    # Build vocabulary
    print("\nBuilding vocabulary...")
    vocab = build_vocab(texts, vocab_size=10000)
    print(f"Vocabulary size: {len(vocab)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, encoded_labels, test_size=0.2, random_state=42, stratify=encoded_labels
    )
    
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # Create datasets
    train_dataset = ExpenseDataset(X_train, y_train, vocab)
    test_dataset = ExpenseDataset(X_test, y_test, vocab)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)
    
    # Initialize model
    num_classes = len(label_encoder.classes_)
    model = ExpenseCNN(
        vocab_size=len(vocab) + 1,
        embedding_dim=128,
        num_classes=num_classes
    ).to(device)
    
    print(f"\nModel architecture:\n{model}")
    print(f"\nTraining on: {device}")
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Training loop
    print("\nStarting training...\n")
    best_accuracy = 0.0
    
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        
        for batch_texts, batch_labels in train_loader:
            batch_texts = batch_texts.to(device)
            batch_labels = batch_labels.squeeze().to(device)
            
            # Forward pass
            outputs = model(batch_texts)
            loss = criterion(outputs, batch_labels)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # Evaluation
        model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for batch_texts, batch_labels in test_loader:
                batch_texts = batch_texts.to(device)
                batch_labels = batch_labels.squeeze().to(device)
                
                outputs = model(batch_texts)
                _, predicted = torch.max(outputs.data, 1)
                
                total += batch_labels.size(0)
                correct += (predicted == batch_labels).sum().item()
        
        accuracy = 100 * correct / total
        avg_loss = train_loss / len(train_loader)
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
        
        if (epoch + 1) % 5 == 0:
            print(f"Epoch [{epoch+1}/{num_epochs}] - Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%")
    
    print(f"\n✓ Training completed!")
    print(f"Best accuracy: {best_accuracy:.2f}%")
    
    # Save model
    save_path = Path(__file__).parent / 'expense_cnn_model.pt'
    
    # Move model to CPU before saving
    model = model.to('cpu')
    
    torch.save({
        'model_state_dict': model.state_dict(),
        'vocab': vocab,
        'label_encoder': label_dict,
        'vocab_size': len(vocab) + 1,
        'embedding_dim': 128,
        'num_classes': num_classes,
    }, save_path)
    
    print(f"\n✓ Model saved to: {save_path}")
    
    return model, vocab, label_dict


if __name__ == "__main__":
    # Train the model
    model, vocab, label_encoder = train_model(
        num_epochs=50,
        batch_size=16,
        learning_rate=0.001
    )
    
    print("\n=== Training Complete ===")
    print("\nYou can now use the model in Django!")
