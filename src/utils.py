"""
Utilities and Visualization Module
Provides helper functions for analysis and visualization
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter


class VisualizationHelper:
    """Helper class for data visualization"""
    
    @staticmethod
    def set_style():
        """Set default matplotlib and seaborn style"""
        sns.set_style("whitegrid")
        sns.set_palette("husl")
    
    @staticmethod
    def plot_word_frequency(word_freq, top_n=20, title="Top Words by Frequency"):
        """Plot top N words by frequency"""
        if isinstance(word_freq, Counter):
            top_words = dict(word_freq.most_common(top_n))
        else:
            top_words = word_freq
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        words = list(top_words.keys())
        frequencies = list(top_words.values())
        
        ax.bar(range(len(words)), frequencies, color='steelblue', alpha=0.8)
        ax.set_xticks(range(len(words)))
        ax.set_xticklabels(words, rotation=45, ha='right')
        ax.set_ylabel('Frequency')
        ax.set_title(title)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_distribution(data, title="Distribution", bins=30):
        """Plot distribution of data"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(data, bins=bins, color='steelblue', alpha=0.7, edgecolor='black')
        ax.set_title(title)
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_performance_comparison(metrics_dict, title="Algorithm Comparison"):
        """Compare performance of different algorithms"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        algorithms = list(metrics_dict.keys())
        metric_names = list(metrics_dict[algorithms[0]].keys())
        
        x = np.arange(len(algorithms))
        width = 0.15
        
        for i, metric in enumerate(metric_names):
            values = [metrics_dict[algo].get(metric, 0) for algo in algorithms]
            ax.bar(x + i * width, values, width, label=metric, alpha=0.8)
        
        ax.set_xlabel('Algorithms')
        ax.set_ylabel('Score')
        ax.set_title(title)
        ax.set_xticks(x + width * (len(metric_names) - 1) / 2)
        ax.set_xticklabels(algorithms)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_confusion_matrix(cm, labels, title="Confusion Matrix"):
        """Plot confusion matrix heatmap"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=labels, yticklabels=labels, ax=ax)
        ax.set_title(title)
        ax.set_ylabel('True Label')
        ax.set_xlabel('Predicted Label')
        
        plt.tight_layout()
        return fig


class PerformanceMetrics:
    """Calculate and track performance metrics"""
    
    @staticmethod
    def recall_at_k(predictions, target, k=5):
        """Calculate recall@k"""
        if len(predictions) == 0:
            return 0.0
        return 1.0 if any(pred == target for pred, _ in predictions[:k]) else 0.0
    
    @staticmethod
    def ndcg_at_k(predictions, target, k=5):
        """Calculate normalized discounted cumulative gain @k"""
        dcg = 0.0
        for rank, (pred, score) in enumerate(predictions[:k], 1):
            if pred == target:
                dcg = 1.0 / np.log2(rank + 1)
                break
        
        # Ideal DCG (assuming relevant item ranks first)
        idcg = 1.0 / np.log2(2)
        return dcg / idcg if idcg > 0 else 0.0
    
    @staticmethod
    def average_rank(predictions, target):
        """Calculate average rank of target in predictions"""
        for rank, (pred, _) in enumerate(predictions, 1):
            if pred == target:
                return rank
        return len(predictions) + 1
    
    @staticmethod
    def f1_score(precision, recall):
        """Calculate F1 score from precision and recall"""
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)


class DataAnalyzer:
    """Analyze processed data"""
    
    @staticmethod
    def get_statistics(data):
        """Get basic statistics about data"""
        stats = {
            'total_samples': len(data),
            'avg_length': data['token_count'].mean() if 'token_count' in data else 0,
            'max_length': data['token_count'].max() if 'token_count' in data else 0,
            'min_length': data['token_count'].min() if 'token_count' in data else 0,
        }
        return stats
    
    @staticmethod
    def get_token_frequency(tokens_list):
        """Get unique tokens and their frequencies"""
        all_tokens = []
        for tokens in tokens_list:
            if isinstance(tokens, list):
                all_tokens.extend(tokens)
            else:
                all_tokens.append(tokens)
        
        return Counter(all_tokens)


def save_results(results_dict, filepath, format='json'):
    """Save results to file"""
    import json
    
    if format == 'json':
        with open(filepath, 'w') as f:
            json.dump(results_dict, f, indent=4)
    elif format == 'csv':
        df = pd.DataFrame(results_dict)
        df.to_csv(filepath, index=False)


def load_results(filepath):
    """Load results from file"""
    import json
    
    if filepath.endswith('.json'):
        with open(filepath, 'r') as f:
            return json.load(f)
    elif filepath.endswith('.csv'):
        return pd.read_csv(filepath)
