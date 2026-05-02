"""
Anomaly Detection Module for Fraud Detection System
"""

import logging
from typing import Dict, Any, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope

import config
from src.utils import setup_logging


class AnomalyDetectionEngine:
    """Multi-method anomaly detection engine."""
    
    def __init__(self):
        """Initialize anomaly detection engine."""
        self.logger = setup_logging(__name__)
        self.detectors = {}
        self.trained = False
    
    def train_isolation_forest(self, X: np.ndarray, contamination: float = None) -> None:
        """
        Train Isolation Forest detector.
        
        Args:
            X: Training features
            contamination: Contamination ratio
        """
        if contamination is None:
            contamination = config.CONTAMINATION_RATIO
        
        self.logger.info(f"Training Isolation Forest with contamination={contamination}")
        
        self.detectors['isolation_forest'] = IsolationForest(
            contamination=contamination,
            random_state=config.RANDOM_STATE,
            n_estimators=100,
            n_jobs=-1
        )
        self.detectors['isolation_forest'].fit(X)
    
    def train_local_outlier_factor(self, X: np.ndarray, contamination: float = None, 
                                   n_neighbors: int = 20) -> None:
        """
        Train Local Outlier Factor detector.
        
        Args:
            X: Training features
            contamination: Contamination ratio
            n_neighbors: Number of neighbors
        """
        if contamination is None:
            contamination = config.CONTAMINATION_RATIO
        
        self.logger.info(f"Training LOF with contamination={contamination}")
        
        self.detectors['lof'] = LocalOutlierFactor(
            contamination=contamination,
            n_neighbors=n_neighbors,
            n_jobs=-1
        )
        self.detectors['lof'].fit(X)
    
    def train_elliptic_envelope(self, X: np.ndarray, contamination: float = None) -> None:
        """
        Train Elliptic Envelope detector (robust covariance).
        
        Args:
            X: Training features
            contamination: Contamination ratio
        """
        if contamination is None:
            contamination = config.CONTAMINATION_RATIO
        
        self.logger.info(f"Training Elliptic Envelope with contamination={contamination}")
        
        self.detectors['elliptic_envelope'] = EllipticEnvelope(
            contamination=contamination,
            random_state=config.RANDOM_STATE
        )
        self.detectors['elliptic_envelope'].fit(X)
    
    def train_all_detectors(self, X: np.ndarray) -> None:
        """
        Train all anomaly detectors.
        
        Args:
            X: Training features
        """
        self.logger.info("Training all anomaly detectors...")
        
        self.train_isolation_forest(X)
        self.train_local_outlier_factor(X)
        self.train_elliptic_envelope(X)
        
        self.trained = True
        self.logger.info(f"Trained {len(self.detectors)} anomaly detectors")
    
    def detect_isolation_forest(self, X: np.ndarray) -> Dict[str, Any]:
        """
        Detect anomalies using Isolation Forest.
        
        Args:
            X: Features to detect
            
        Returns:
            Dictionary with predictions and scores
        """
        if 'isolation_forest' not in self.detectors:
            raise ValueError("Isolation Forest not trained")
        
        detector = self.detectors['isolation_forest']
        predictions = detector.predict(X)  # -1: anomaly, 1: normal
        scores = detector.score_samples(X)  # negative: anomaly, positive: normal
        
        return {
            'predictions': predictions,
            'scores': scores,
            'anomalies': (predictions == -1).astype(int),
            'anomaly_scores': -scores  # Invert so higher = more anomalous
        }
    
    def detect_lof(self, X: np.ndarray) -> Dict[str, Any]:
        """
        Detect anomalies using Local Outlier Factor.
        
        Args:
            X: Features to detect
            
        Returns:
            Dictionary with predictions and scores
        """
        if 'lof' not in self.detectors:
            raise ValueError("LOF not trained")
        
        detector = self.detectors['lof']
        predictions = detector.predict(X)  # -1: anomaly, 1: normal
        scores = detector.negative_outlier_factor_  # Lower = more anomalous
        
        # Get LOF scores for test data
        lof_scores = detector._local_outlier_factor[detector._fit_X]
        
        return {
            'predictions': predictions,
            'anomalies': (predictions == -1).astype(int),
        }
    
    def detect_elliptic_envelope(self, X: np.ndarray) -> Dict[str, Any]:
        """
        Detect anomalies using Elliptic Envelope.
        
        Args:
            X: Features to detect
            
        Returns:
            Dictionary with predictions and scores
        """
        if 'elliptic_envelope' not in self.detectors:
            raise ValueError("Elliptic Envelope not trained")
        
        detector = self.detectors['elliptic_envelope']
        predictions = detector.predict(X)  # -1: anomaly, 1: normal
        scores = detector.score_samples(X)
        
        return {
            'predictions': predictions,
            'scores': scores,
            'anomalies': (predictions == -1).astype(int),
            'anomaly_scores': -scores  # Invert so higher = more anomalous
        }
    
    def detect_all(self, X: np.ndarray) -> Dict[str, Dict[str, Any]]:
        """
        Detect anomalies using all methods.
        
        Args:
            X: Features to detect
            
        Returns:
            Dictionary with results from all detectors
        """
        if not self.trained:
            raise ValueError("Detectors not trained yet")
        
        results = {
            'isolation_forest': self.detect_isolation_forest(X),
            'lof': self.detect_lof(X),
            'elliptic_envelope': self.detect_elliptic_envelope(X),
        }
        
        return results
    
    def ensemble_detection(self, X: np.ndarray, voting_threshold: float = 2) -> np.ndarray:
        """
        Ensemble anomaly detection using voting.
        
        Args:
            X: Features to detect
            voting_threshold: Number of detectors that must agree (1-3)
            
        Returns:
            Binary anomaly predictions
        """
        if not self.trained:
            raise ValueError("Detectors not trained yet")
        
        results = self.detect_all(X)
        
        # Collect anomaly predictions
        votes = np.zeros(X.shape[0])
        for detector_name, result in results.items():
            votes += result['anomalies']
        
        # Convert to binary: anomaly if votes >= threshold
        ensemble_predictions = (votes >= voting_threshold).astype(int)
        
        return ensemble_predictions
    
    def get_anomaly_probability(self, X: np.ndarray) -> np.ndarray:
        """
        Get probability of being anomaly based on ensemble voting.
        
        Args:
            X: Features to detect
            
        Returns:
            Anomaly probabilities
        """
        if not self.trained:
            raise ValueError("Detectors not trained yet")
        
        results = self.detect_all(X)
        
        # Average votes across detectors
        votes = np.zeros(X.shape[0])
        for detector_name, result in results.items():
            votes += result['anomalies']
        
        # Normalize to probability
        anomaly_proba = votes / len(results)
        
        return anomaly_proba


if __name__ == "__main__":
    logger = setup_logging(__name__)
    logger.info("Anomaly Detection module loaded successfully")
