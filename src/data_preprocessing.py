"""
Data Preprocessing Module
Handles cleaning and preparing text data for NLP analysis
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class TextPreprocessor:
    """Clean and preprocess text data for NLP tasks"""
    
    def __init__(self, remove_stopwords=False, lowercase=True):
        self.remove_stopwords = remove_stopwords
        self.lowercase = lowercase
        self.stop_words = set(stopwords.words('english')) if remove_stopwords else set()
    
    def clean_text(self, text):
        """
        Clean text by removing special characters, extra whitespace, etc.
        
        Args:
            text (str): Raw text to clean
        
        Returns:
            str: Cleaned text
        """
        if not isinstance(text, str):
            return ""
        
        # Lowercase
        if self.lowercase:
            text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and digits (optional)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def tokenize(self, text):
        """Tokenize text into words"""
        return word_tokenize(text)
    
    def remove_stopwords_func(self, tokens):
        """Remove stopwords from token list"""
        if self.remove_stopwords:
            return [token for token in tokens if token.lower() not in self.stop_words]
        return tokens
    
    def preprocess_batch(self, texts):
        """Preprocess a batch of texts"""
        return [self.clean_text(text) for text in texts]


class DataLoader:
    """Load and prepare datasets for analysis"""
    
    @staticmethod
    def load_csv(filepath):
        """Load CSV file"""
        return pd.read_csv(filepath)
    
    @staticmethod
    def load_text_file(filepath):
        """Load text file and return as list of lines"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()
    
    @staticmethod
    def create_dataset_from_text(texts, sample_size=None):
        """
        Create dataset from list of texts
        
        Args:
            texts (list): List of text strings
            sample_size (int): Number of samples to use (None for all)
        
        Returns:
            DataFrame: Dataset with cleaned and tokenized texts
        """
        if sample_size:
            texts = texts[:sample_size]
        
        processor = TextPreprocessor()
        data = []
        
        for text in texts:
            cleaned = processor.clean_text(text)
            tokens = processor.tokenize(cleaned)
            data.append({
                'original': text,
                'cleaned': cleaned,
                'tokens': tokens,
                'token_count': len(tokens)
            })
        
        return pd.DataFrame(data)


def generate_sample_data(num_samples=1000):
    """Generate sample autocorrect/autocomplete data"""
    sample_texts = [
        "coffee machine is broken",
        "I need to fix my spelling",
        "autocomplete saves time",
        "machine learning is awesome",
        "natural language processing",
        "data science and analytics",
        "python programming language",
        "artificial intelligence revolution",
        "deep learning networks",
        "neural network training"
    ]
    
    # Repeat and shuffle to create dataset
    np.random.seed(42)
    texts = np.random.choice(sample_texts, num_samples)
    return texts
