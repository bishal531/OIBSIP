"""
Autocomplete Module
Implements various autocomplete algorithms for word/phrase prediction
"""

import re
from collections import defaultdict, Counter
from typing import List, Tuple, Dict
import numpy as np


class TrieNode:
    """Node in a Trie data structure"""
    def __init__(self):
        self.children = {}
        self.is_word = False
        self.frequency = 0


class TrieautocompleteEngine:
    """Autocomplete using Trie data structure"""
    
    def __init__(self):
        self.root = TrieNode()
        self.vocabulary = set()
    
    def insert(self, word, frequency=1):
        """Insert word into Trie with frequency"""
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_word = True
        node.frequency += frequency
        self.vocabulary.add(word.lower())
    
    def build_from_text(self, words):
        """Build Trie from list of words"""
        word_freq = Counter(words)
        for word, freq in word_freq.items():
            self.insert(word, freq)
    
    def get_predictions(self, prefix, max_results=10):
        """Get autocomplete predictions for a prefix"""
        node = self.root
        prefix = prefix.lower()
        
        # Navigate to prefix node
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # DFS to find all words starting with prefix
        predictions = []
        self._dfs(node, prefix, predictions)
        
        # Sort by frequency
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:max_results]
    
    def _dfs(self, node, current_word, predictions):
        """Depth-first search to find all words"""
        if node.is_word:
            predictions.append((current_word, node.frequency))
        
        for char, child_node in node.children.items():
            self._dfs(child_node, current_word + char, predictions)


class NGramAutocomplete:
    """Autocomplete using N-gram language model"""
    
    def __init__(self, n=3):
        self.n = n
        self.ngrams = defaultdict(lambda: defaultdict(int))
        self.word_freq = Counter()
    
    def train(self, tokens):
        """Train N-gram model from token list"""
        self.word_freq = Counter(tokens)
        
        # Create n-grams
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i + self.n - 1])
            next_word = tokens[i + self.n - 1]
            self.ngrams[ngram][next_word] += 1
    
    def predict_next_word(self, prefix_tokens, top_k=5):
        """Predict next word given prefix tokens"""
        if len(prefix_tokens) < self.n - 1:
            # Not enough context, return most common words
            return [(word, count) for word, count in self.word_freq.most_common(top_k)]
        
        # Get last n-1 tokens as context
        context = tuple(prefix_tokens[-(self.n - 1):])
        
        if context in self.ngrams:
            predictions = sorted(
                self.ngrams[context].items(),
                key=lambda x: x[1],
                reverse=True
            )
            return predictions[:top_k]
        
        return []
    
    def predict_phrase(self, prefix, tokens, max_length=5):
        """Predict complete phrase given prefix"""
        phrase = prefix.copy()
        
        for _ in range(max_length - len(prefix)):
            next_words = self.predict_next_word(phrase, top_k=1)
            if not next_words:
                break
            phrase.append(next_words[0][0])
        
        return phrase


class FrequencybasedAutocomplete:
    """Simple frequency-based autocomplete"""
    
    def __init__(self):
        self.word_freq = Counter()
        self.vocabulary = {}
    
    def train(self, words):
        """Train on word frequencies"""
        self.word_freq = Counter(words)
        self.vocabulary = {word: freq for word, freq in self.word_freq.items()}
    
    def predict(self, prefix, top_k=10):
        """Predict words matching prefix"""
        prefix = prefix.lower()
        matches = []
        
        for word, freq in self.vocabulary.items():
            if word.startswith(prefix):
                matches.append((word, freq))
        
        # Sort by frequency
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_k]
    
    def similarity_score(self, word1, word2):
        """Calculate similarity between two words"""
        # Jaccard similarity
        set1 = set(word1)
        set2 = set(word2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0
    
    def fuzzy_predict(self, prefix, threshold=0.6, top_k=10):
        """Fuzzy autocomplete using similarity"""
        matches = []
        prefix = prefix.lower()
        
        for word in self.vocabulary.keys():
            similarity = self.similarity_score(prefix, word)
            if similarity >= threshold:
                score = similarity * self.vocabulary[word]
                matches.append((word, score))
        
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_k]


class AutocompleteEvaluator:
    """Evaluate autocomplete performance"""
    
    @staticmethod
    def mean_reciprocal_rank(predictions, target):
        """Calculate Mean Reciprocal Rank"""
        for rank, (pred, _) in enumerate(predictions, 1):
            if pred == target:
                return 1.0 / rank
        return 0.0
    
    @staticmethod
    def precision_at_k(predictions, target, k=5):
        """Calculate Precision@K"""
        return 1.0 if any(pred == target for pred, _ in predictions[:k]) else 0.0
    
    @staticmethod
    def evaluate_batch(model, test_data, target_column='target'):
        """Evaluate model on batch of test data"""
        mrr_scores = []
        precision_scores = []
        
        for idx, row in test_data.iterrows():
            prefix = row['prefix']
            target = row[target_column]
            
            predictions = model.predict(prefix, top_k=5) if hasattr(model, 'predict') else []
            
            mrr = AutocompleteEvaluator.mean_reciprocal_rank(predictions, target)
            precision = AutocompleteEvaluator.precision_at_k(predictions, target)
            
            mrr_scores.append(mrr)
            precision_scores.append(precision)
        
        return {
            'mean_reciprocal_rank': np.mean(mrr_scores),
            'precision_at_5': np.mean(precision_scores)
        }
