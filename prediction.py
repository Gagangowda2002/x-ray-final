"""
Prediction utilities
"""
import numpy as np
import tensorflow as tf
from logger import get_logger

logger = get_logger(__name__)

class PredictionEngine:
    """Handles model predictions and results"""
    
    # Class names aligned with training dataset class_indices
    CLASS_NAMES = [
        "Avulsion fracture",
        "Comminuted fracture",
        "Compression-Crush fracture",
        "Fracture Dislocation",
        "Greenstick fracture",
        "Hairline Fracture",
        "Impacted fracture",
        "Intra-articular fracture",
        "Longitudinal fracture",
        "Oblique fracture",
        "Pathological fracture",
        "Spiral Fracture"
    ]
    
    def __init__(self, model_path):
        """
        Initialize prediction engine with model
        
        Args:
            model_path: Path to the saved model
        """
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the model from disk"""
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            logger.info(f"Model loaded successfully from {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise RuntimeError(f"Failed to load model: {str(e)}")
    
    def predict(self, image_array):
        """
        Make prediction on image
        
        Args:
            image_array: Preprocessed image array (batch format)
        
        Returns:
            dict: Prediction results with class, confidence, and probabilities
        """
        try:
            if self.model is None:
                raise RuntimeError("Model not loaded")
            
            # Get predictions
            predictions = self.model.predict(image_array, verbose=0)[0]
            
            # Top classes
            top_indices = np.argsort(predictions)[::-1]
            pred_class_idx = int(top_indices[0])
            second_class_idx = int(top_indices[1])
            raw_confidence = float(predictions[pred_class_idx])
            second_confidence = float(predictions[second_class_idx])
            pred_class = self.CLASS_NAMES[pred_class_idx]

            # Confidence diagnostics: margin + normalized entropy
            margin = raw_confidence - second_confidence
            entropy = -np.sum(predictions * np.log(predictions + 1e-12))
            normalized_entropy = float(entropy / np.log(len(predictions)))

            # Heuristic calibration to reduce overconfidence on out-of-domain images
            margin_factor = float(min(1.0, max(0.0, margin / 0.35)))
            entropy_factor = float(max(0.0, 1.0 - normalized_entropy))
            calibrated_confidence = float(
                raw_confidence * (0.55 + 0.25 * margin_factor + 0.20 * entropy_factor)
            )

            is_reliable = bool(
                raw_confidence >= 0.65 and margin >= 0.20 and normalized_entropy <= 0.55
            )

            warning_message = None
            if not is_reliable:
                warning_message = (
                    "Low reliability prediction: uploaded image may be out-of-distribution "
                    "or uncertain for this model."
                )

            display_class = pred_class
            if not is_reliable:
                display_class = "Unknown / Not an X-ray"
            
            # Get top 3 predictions
            top_3_indices = top_indices[:3]
            top_predictions = [
                {
                    'class': self.CLASS_NAMES[idx],
                    'confidence': float(predictions[idx]) * 100
                }
                for idx in top_3_indices
            ]
            
            result = {
                'class': pred_class,
                'display_class': display_class,
                'class_index': pred_class_idx,
                'confidence': calibrated_confidence * 100,
                'confidence_score': calibrated_confidence,
                'raw_confidence': raw_confidence * 100,
                'margin': margin,
                'normalized_entropy': normalized_entropy,
                'is_reliable': is_reliable,
                'warning_message': warning_message,
                'probabilities': {self.CLASS_NAMES[i]: float(predictions[i]) * 100 
                                  for i in range(len(self.CLASS_NAMES))},
                'top_3_predictions': top_predictions
            }
            
            logger.info(
                "Prediction successful: %s | calibrated=%.2f%% | raw=%.2f%% | margin=%.3f | entropy=%.3f | reliable=%s",
                pred_class,
                calibrated_confidence * 100,
                raw_confidence * 100,
                margin,
                normalized_entropy,
                is_reliable,
            )
            return result
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise RuntimeError(f"Prediction error: {str(e)}")
    
    def get_class_names(self):
        """Get list of all class names"""
        return self.CLASS_NAMES
