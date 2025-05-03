import tensorflow as tf
from PIL import Image
import numpy as np
import io
import logging
from threading import Lock
import functools
import hashlib

# Define class labels
class_labels = ["Benign", "Malignant"]  # Update if you have more/different classes

# Global model and thread lock
model = None
model_lock = Lock()

def get_model():
    global model
    if model is None:
        with model_lock:
            if model is None:
                try:
                    # Load model with optimized settings
                    model = tf.keras.models.load_model("my_model.keras")
                    logging.info("Model loaded successfully.")
                except Exception as e:
                    logging.error(f"Model loading failed: {e}")
                    raise RuntimeError("Failed to load model.")
    return model

# Cache for predictions (LRU cache with maxsize=100)
@functools.lru_cache(maxsize=100)
def predict_cached(image_hash):
    # This function will be called only when there's a cache miss
    return predict_image_impl(image_cache.get(image_hash))

# Cache for image data
image_cache = {}

def predict_image(file_bytes: bytes) -> dict:
    # Create a hash of the image bytes for caching
    image_hash = hashlib.md5(file_bytes).hexdigest()

    # Store the image bytes in the image cache
    image_cache[image_hash] = file_bytes

    # Use the cached prediction function
    result = predict_cached(image_hash)

    # Clean up the image cache if the prediction is cached
    if len(image_cache) > 100:
        # Remove the oldest entries when cache gets too large
        old_keys = list(image_cache.keys())[:-100]
        for key in old_keys:
            image_cache.pop(key, None)

    return result

def predict_image_impl(file_bytes: bytes) -> dict:
    # Use a context manager for the image to ensure proper resource cleanup
    with Image.open(io.BytesIO(file_bytes)) as image:
        image = image.convert("RGB")

        # Convert to array and normalize more efficiently
        img_array = np.asarray(image, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Lazy load model and predict
    model_instance = get_model()

    # Use TensorFlow's optimized prediction
    prediction = model_instance.predict(img_array, verbose=0)[0]
    class_index = np.argmax(prediction)
    confidence = float(prediction[class_index])

    return {
        "class": class_labels[class_index],
        "confidence": round(confidence, 4)
    }
