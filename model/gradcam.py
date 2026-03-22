
import tensorflow as tf
import numpy as np
import cv2

def generate_gradcam(model, img_array):
    """
    Generate Grad-CAM heatmap for DenseNet model
    
    Args:
        model: Keras model
        img_array: Input image array (preprocessed)
    
    Returns:
        Heatmap array normalized to [0, 1]
    """
    try:
        # Find the last convolutional layer dynamically
        last_conv_layer = None
        for layer in reversed(model.layers):
            if 'conv' in layer.name.lower() and len(layer.output.shape) == 4:
                last_conv_layer = layer
                break
        
        if last_conv_layer is None:
            # Fallback for models without conv layers (shouldn't happen with DenseNet)
            print("Warning: Could not find convolutional layer, returning zeros")
            return np.zeros((224, 224))
        
        # Create model with last conv layer and predictions as outputs
        grad_model = tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[last_conv_layer.output, model.output]
        )
        
        # Compute gradients
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array, training=False)
            # Get the prediction for the predicted class
            pred_index = tf.argmax(predictions[0])
            class_channel = predictions[:, pred_index]
        
        grads = tape.gradient(class_channel, conv_outputs)
        
        if grads is None:
            print("Warning: Gradient is None, returning zeros")
            return np.zeros((224, 224))
        
        # Pool gradients
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Generate heatmap
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        
        # Normalize heatmap
        heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-10)
        
        return heatmap.numpy()
    
    except Exception as e:
        print(f"Error generating Grad-CAM: {str(e)}")
        return np.zeros((224, 224))

def overlay_heatmap(original_path, heatmap, output_path):
    """
    Overlay heatmap on original image
    
    Args:
        original_path: Path to original image
        heatmap: Grad-CAM heatmap array
        output_path: Path to save overlay image
    """
    try:
        img = cv2.imread(original_path)
        
        if img is None:
            print(f"Error: Could not read image at {original_path}")
            return
        
        # Resize heatmap to match image size
        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        
        # Overlay heatmap on image
        superimposed_img = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
        cv2.imwrite(output_path, superimposed_img)
    
    except Exception as e:
        print(f"Error overlaying heatmap: {str(e)}")
