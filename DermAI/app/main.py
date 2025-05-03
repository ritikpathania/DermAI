from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from .model import predict_image
import os
import logging

# Suppress TensorFlow logs (optional but recommended on Render)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>DermAI</title></head>
        <body style="text-align:center; font-family: Arial;">
            <h1>Welcome to DermAI 🌟</h1>
            <p>Upload a skin lesion image at <a href="/docs" target="_blank">/docs</a> to get a prediction.</p>
        </body>
    </html>
    """

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large. Max size is 10MB.")

        # Use the predict_image function from model.py
        result = predict_image(contents)

        # Map the result to match the expected format in gradio_app.py
        class_name = result["class"]
        confidence = result["confidence"]

        # Convert class name to integer (0 for Benign, 1 for Malignant)
        predicted_class = 0 if class_name == "Benign" else 1

        return {
            "prediction": predicted_class,
            "probability": confidence
        }

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=400,
            detail="Failed to process the image or make a prediction. Please try again with a valid image."
        )
