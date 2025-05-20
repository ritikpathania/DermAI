import sys
import os
import threading
import uvicorn
from .gradio_app import demo
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from .model import predict_image
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# Function to start FastAPI in a separate thread
def start_fastapi():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)  # Adjust the path if necessary

# Function to start Gradio
def start_gradio():
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        share=os.environ.get("SHARE_APP", "false").lower() == "true",
        favicon_path='app/static/DermAI_favicon.png'
    )

if __name__ == "__main__":
    # Start FastAPI in a separate thread (non-daemon so it keeps running)
    fastapi_thread = threading.Thread(target=start_fastapi, daemon=False)
    fastapi_thread.start()

    # Start Gradio in a separate thread
    gradio_thread = threading.Thread(target=start_gradio, daemon=False)
    gradio_thread.start()

    # Keep the main thread running
    try:
        # This will keep the main thread alive
        fastapi_thread.join()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        # The threads will be terminated when the main process exits