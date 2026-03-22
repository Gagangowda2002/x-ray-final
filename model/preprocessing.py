
import cv2
import numpy as np

IMG_SIZE = (224, 224)

def preprocess_image(image_path):
    """
    Preprocess image for model prediction
    
    Args:
        image_path: Path to image file
    
    Returns:
        Preprocessed image array with shape (1, 224, 224, 3)
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        
        if img is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Convert BGR to RGB if needed
        if len(img.shape) == 3 and img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Handle grayscale images
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        
        # Resize to expected size
        img = cv2.resize(img, IMG_SIZE)
        
        # Normalize pixel values
        img = img.astype("float32") / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    
    except Exception as e:
        print(f"Error preprocessing image: {str(e)}")
        raise RuntimeError(f"Failed to preprocess image: {str(e)}")
