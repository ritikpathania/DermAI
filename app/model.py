import tensorflow as tf
from PIL import Image
import numpy as np
import io
import logging
from threading import Lock
import functools
import hashlib
import os
import gdown

# Define class labels
class_labels = ["Benign", "Malignant"]

# Global model and thread lock
model = None
model_lock = Lock()

# Path to model file and Google Drive ID
MODEL_FILENAME = "my_model.keras"
DRIVE_FILE_ID = "1NTUzq3UNIyrG7Ow5NXQojoz8wZXnT8cl"
MODEL_URL = f"https://drive.google.com/uc?id={DRIVE_FILE_ID}"

def download_model_if_not_exists():
    if not os.path.exists(MODEL_FILENAME):
        logging.info("Model file not found locally. Downloading from Google Drive...")
        try:
            gdown.download(MODEL_URL, MODEL_FILENAME, quiet=False)
            logging.info("Model downloaded successfully.")
        except Exception as e:
            logging.error(f"Failed to download model: {e}")
            raise RuntimeError("Model download failed.")

def get_model():
    global model
    if model is None:
        with model_lock:
            if model is None:
                download_model_if_not_exists()
                try:
                    model = tf.keras.models.load_model(MODEL_FILENAME)
                    logging.info("Model loaded successfully.")
                except Exception as e:
                    logging.error(f"Model loading failed: {e}")
                    raise RuntimeError("Failed to load model.")
    return model

# Cache for predictions
@functools.lru_cache(maxsize=100)
def predict_cached(image_hash):
    return predict_image_impl(image_cache.get(image_hash))

# Cache for image data
image_cache = {}

def predict_image(file_bytes: bytes) -> dict:
    image_hash = hashlib.md5(file_bytes).hexdigest()
    image_cache[image_hash] = file_bytes
    result = predict_cached(image_hash)

    if len(image_cache) > 100:
        old_keys = list(image_cache.keys())[:-100]
        for key in old_keys:
            image_cache.pop(key, None)

    return result

def predict_image_impl(file_bytes: bytes) -> dict:
    with Image.open(io.BytesIO(file_bytes)) as image:
        image = image.convert("RGB")

        # ✅ Resize image to match model input
        image = image.resize((224, 224))

        img_array = np.asarray(image, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

    model_instance = get_model()
    prediction = model_instance.predict(img_array, verbose=0)[0]
    class_index = np.argmax(prediction)
    confidence = float(prediction[class_index])

    return {
        "class": class_labels[class_index],
        "confidence": round(confidence, 4)
    }
