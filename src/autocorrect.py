"""
Autocorrect Module
Implements various autocorrect algorithms for spelling error correction
"""

from textblob import TextBlob
import difflib
from collections import Counter
from typing import List, Tuple, Dict
import numpy as np
import re


class SimpleAutocorrect:
    """Simple autocorrect using TextBlob"""
    
    def __init__(self):
        self.corpus = []
    
    def train(self, texts):
        """Train on a corpus of texts"""
        self.corpus = texts
    
    def correct_text(self, text):
        """Correct text using TextBlob"""
        blob = TextBlob(text)
        return str(blob.correct())
    
    def correct_word(self, word):
        """Correct a single word"""
        blob = TextBlob(word)
        return str(blob.correct())


class EditDistanceAutocorrect:
    """Autocorrect using Edit Distance (Levenshtein Distance)"""
    
    def __init__(self, vocabulary=None, max_distance=2):
        self.vocabulary = set(vocabulary) if vocabulary else set()
        self.word_freq = Counter()
        self.max_distance = max_distance
    
    def train(self, words):
        """Train on word list and frequencies"""
        self.word_freq = Counter(words)
        self.vocabulary = set(words)
    
    def levenshtein_distance(self, word1, word2):
        """Calculate Levenshtein distance between two words"""
        len1, len2 = len(word1), len(word2)
        
        # Create DP table
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        
        # Initialize
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j
        
        # Fill DP table
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j],      # deletion
                                       dp[i][j - 1],      # insertion
                                       dp[i - 1][j - 1])  # substitution
        
        return dp[len1][len2]
    
    def get_candidates(self, word, max_distance=None):
        """Get candidate corrections within max edit distance"""
        if max_distance is None:
            max_distance = self.max_distance
        
        candidates = []
        for vocab_word in self.vocabulary:
            dist = self.levenshtein_distance(word.lower(), vocab_word.lower())
            if dist <= max_distance:
                candidates.append((vocab_word, dist, self.word_freq[vocab_word]))
        
        # Sort by distance then frequency
        candidates.sort(key=lambda x: (x[1], -x[2]))
        return candidates
    
    def correct_word(self, word, top_k=5):
        """Correct a word and return top candidates"""
        if word in self.vocabulary:
            return [(word, 0)]
        
        candidates = self.get_candidates(word)
        return candidates[:top_k]
    
    def correct_text(self, text):
        """Correct text by correcting each word"""
        words = text.split()
        corrected_words = []
        
        for word in words:
            # Remove punctuation for correction
            clean_word = re.sub(r'[^\w]', '', word)
            matched_punctuation = ''.join(re.findall(r'[^\w]', word))
            
            if clean_word in self.vocabulary:
                corrected_words.append(word)
            else:
                candidates = self.correct_word(clean_word, top_k=1)
                if candidates:
                    corrected_word = candidates[0][0] + matched_punctuation
                    corrected_words.append(corrected_word)
                else:
                    corrected_words.append(word)
        
        return ' '.join(corrected_words)


class ContextawareAutocorrect:
    """Autocorrect using context from surrounding words"""
    
    def __init__(self, vocabulary=None):
        self.vocabulary = set(vocabulary) if vocabulary else set()
        self.word_freq = Counter()
        self.context_freq = {}
    
    def train(self, words, context_window=2):
        """Train on words with context"""
        self.word_freq = Counter(words)
        self.vocabulary = set(words)
        
        # Build context co-occurrence matrix
        self.context_freq = {}
        for i in range(len(words)):
            word = words[i]
            context_words = words[max(0, i-context_window):i] + words[i+1:min(len(words), i+context_window+1)]
            
            if word not in self.context_freq:
                self.context_freq[word] = Counter()
            self.context_freq[word].update(context_words)
    
    def score_correction(self, misspelled, candidate, context_words):
        """Score a candidate correction based on context"""
        # Base frequency score
        freq_score = self.word_freq.get(candidate, 1)
        
        # Context similarity score
        context_score = 0
        if candidate in self.context_freq:
            for ctx_word in context_words:
                context_score += self.context_freq[candidate].get(ctx_word, 0)
        
        # Combined score
        return freq_score + context_score * 0.5
    
    def correct_with_context(self, text, max_distance=2):
        """Correct text considering context"""
        words = text.split()
        corrected_words = []
        
        autocorrect = EditDistanceAutocorrect(self.vocabulary, max_distance)
        autocorrect.word_freq = self.word_freq
        
        for i, word in enumerate(words):
            if word in self.vocabulary:
                corrected_words.append(word)
            else:
                # Get context
                context = words[max(0, i-2):i] + words[i+1:min(len(words), i+3)]
                
                # Get candidates
                candidates = autocorrect.get_candidates(word, max_distance)
                
                if candidates:
                    # Score candidates with context
                    scored = [(cand, self.score_correction(word, cand, context)) 
                             for cand, _, _ in candidates]
                    scored.sort(key=lambda x: x[1], reverse=True)
                    corrected_words.append(scored[0][0])
                else:
                    corrected_words.append(word)
        
        return ' '.join(corrected_words)


class AutocorrectEvaluator:
    """Evaluate autocorrect performance"""
    
    @staticmethod
    def accuracy(predictions, targets):
        """Calculate accuracy of corrections"""
        if len(predictions) == 0:
            return 0.0
        return sum(p == t for p, t in zip(predictions, targets)) / len(predictions)
    
    @staticmethod
    def word_error_rate(original_text, corrected_text):
        """Calculate word error rate between original and corrected text"""
        original_words = original_text.split()
        corrected_words = corrected_text.split()
        
        errors = sum(1 for o, c in zip(original_words, corrected_words) if o != c)
        return errors / len(original_words) if original_words else 0.0
    
    @staticmethod
    def character_error_rate(original_text, corrected_text):
        """Calculate character error rate"""
        errors = 0
        max_len = max(len(original_text), len(corrected_text))
        
        for i in range(max_len):
            o_char = original_text[i] if i < len(original_text) else ' '
            c_char = corrected_text[i] if i < len(corrected_text) else ' '
            if o_char != c_char:
                errors += 1
        
        return errors / max_len if max_len > 0 else 0.0
    
    @staticmethod
    def evaluate_batch(model, test_cases):
        """Evaluate model on batch of test cases"""
        accuracies = []
        wer_scores = []
        cer_scores = []
        
        for original, target in test_cases:
            if hasattr(model, 'correct_text'):
                corrected = model.correct_text(original)
            else:
                corrected = original
            
            acc = AutocorrectEvaluator.accuracy([corrected], [target])
            wer = AutocorrectEvaluator.word_error_rate(original, corrected)
            cer = AutocorrectEvaluator.character_error_rate(original, corrected)
            
            accuracies.append(acc)
            wer_scores.append(wer)
            cer_scores.append(cer)
        
        return {
            'accuracy': np.mean(accuracies),
            'word_error_rate': np.mean(wer_scores),
            'character_error_rate': np.mean(cer_scores)
        }
