import gradio as gr
import requests
import os
import functools
import hashlib
import logging
from pathlib import Path

# --- Configuration ---
# Make API URL configurable through environment variables
API_URL = os.environ.get("DERMAI_API_URL", "http://127.0.0.1:8000/predict")
SERVER_HOST = os.environ.get("DERMAI_HOST", "127.0.0.1")
SERVER_PORT = int(os.environ.get("DERMAI_PORT", "7860"))

# --- HTML Templates ---
# Define HTML templates for different card states
NEUTRAL_CARD = """<div class="card neutral">
                    <div class="icon">💡</div>
                    <div><strong>{message}</strong></div>
                  </div>"""

ERROR_CARD = """<div class="card error">
                <div class="icon">❌</div>
                <div><strong>{message}</strong></div>
              </div>"""

RESULT_CARD_TEMPLATE = """<div class="card {card_class}">
                            <div class="icon">{icon}</div>
                            <div><strong>{result}</strong></div>
                            <div class="confidence">Confidence: {confidence:.2%}</div>
                          </div>"""

# --- Prediction function with caching ---
# Cache for storing prediction results
prediction_cache = {}

@functools.lru_cache(maxsize=50)
def get_cached_prediction(image_hash):
    """Get prediction from cache based on image hash"""
    return prediction_cache.get(image_hash)

def classify(image):
    """Classify a skin lesion image"""
    # Handle empty input
    if image is None:
        return NEUTRAL_CARD.format(message="Please upload a lesion image to analyze.")

    try:
        # Calculate hash of the image for caching
        with open(image, "rb") as img_file:
            image_bytes = img_file.read()
            image_hash = hashlib.md5(image_bytes).hexdigest()

        # Check if prediction is in cache
        cached_result = get_cached_prediction(image_hash)
        if cached_result:
            logging.info(f"Using cached prediction for {image}")
            return cached_result

        # Make an API request with proper resource management
        with open(image, "rb") as img:
            try:
                res = requests.post(API_URL, files={"file": img}, timeout=10)
            except requests.RequestException as e:
                logging.error(f"API request failed: {e}")
                return ERROR_CARD.format(message="Connection error. Please try again.")

        # Handle API errors
        if res.status_code != 200:
            error_msg = f"Error during prediction (Status: {res.status_code})"
            logging.error(error_msg)
            return ERROR_CARD.format(message=error_msg)

        # Process successful response
        data = res.json()
        prediction = data["prediction"]
        confidence = data["probability"]

        # Generate result HTML based on prediction
        if prediction == 0:
            result_html = RESULT_CARD_TEMPLATE.format(
                card_class="success",
                icon="✅",
                result="Benign (Non-cancerous)",
                confidence=confidence
            )
        elif prediction == 1:
            result_html = RESULT_CARD_TEMPLATE.format(
                card_class="warning",
                icon="⚠️",
                result="Malignant (Cancerous)",
                confidence=confidence
            )
        else:
            result_html = NEUTRAL_CARD.format(message="Unknown prediction result.")

        # Cache the result
        prediction_cache[image_hash] = result_html

        # Clean up the cache if it gets too large
        if len(prediction_cache) > 50:
            # Remove oldest entries
            old_keys = list(prediction_cache.keys())[:-50]
            for key in old_keys:
                prediction_cache.pop(key, None)

        return result_html

    except Exception as e:
        logging.error(f"Error in classify function: {e}")
        return ERROR_CARD.format(message="An error occurred during processing.")

# --- Load CSS from external file ---
def load_css():
    """Load CSS from an external file"""
    base_path = Path(os.path.dirname(__file__))
    css_path = base_path / "static" / "styles.css"
    if css_path.exists():
        return css_path.read_text()
    else:
        logging.warning(f"CSS file not found at {css_path}. Using default styles.")
        return ""

# Load CSS from the file
css = load_css()

# --- Gradio UI ---
def create_ui():
    """Create and configure the Gradio UI"""
    with gr.Blocks(css=css, title="DermAI - Skin Lesion Analysis") as demo:
        # Logo and header
        with gr.Row(elem_classes=["logo-container"]):
            gr.Image('app/static/DermAI_logo.png', show_label=False, show_download_button=False,
                     container=False, height=150)

        gr.HTML("<h2>skin lesion analysis powered by deep learning</h2>")

        # Two-column layout using Gradio's Row component
        with gr.Row(elem_classes=["main-wrapper"]):
            # Left column - Image upload
            with gr.Column(elem_id="upload-section", elem_classes=["flex-child"]):
                image = gr.Image(
                    type="filepath", 
                    label="Upload Lesion Image", 
                    elem_classes=["gradio-file-input"],
                    # Set image processing parameters for better performance
                    image_mode="RGB",
                    sources=["upload", "webcam", "clipboard"]
                )
                button = gr.Button("Analyze", elem_id="analyze-btn")

            # Right column - Results
            with gr.Column(elem_id="result-section", elem_classes=["flex-child"]):
                result = gr.HTML(
                    value=NEUTRAL_CARD.format(message="Upload an image to begin diagnosis.")
                )

        # Footer
        gr.HTML("""<div class="footer">
            © 2025 DermAI • Built with ❤️ by Ritik & Trusha
        </div>""")

        # Event handlers
        button.click(fn=classify, inputs=image, outputs=result)

        # Add keyboard shortcut for better UX - removed _js parameter as it's not supported in Gradio 5.28.0
        image.change(fn=lambda: None, inputs=None, outputs=None)

    return demo

# Create the UI
demo = create_ui()

if __name__ == "__main__":

    # Launch the app with configurable settings
    demo.launch(
        server_name=SERVER_HOST, 
        server_port=SERVER_PORT,
        show_error=True,
        share=os.environ.get("SHARE_APP", "false").lower() == "true",
        favicon_path='static/DermAI_favicon.png'
    )
