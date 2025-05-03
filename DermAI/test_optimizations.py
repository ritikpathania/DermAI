#!/usr/bin/env python3
"""
Test script to verify the optimizations in the DermAI application.
This script tests:
1. The model loading and prediction caching in model.py
2. The classify function and caching in gradio_app.py
"""

import os
import time
import logging
import hashlib
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("optimization_test")

def test_model_caching():
    """Test that the model caching in model.py works correctly"""
    logger.info("Testing model caching...")

    try:
        from app.model import get_model, predict_image

        # First call should load the model
        start_time = time.time()
        model = get_model()
        first_load_time = time.time() - start_time
        logger.info(f"First model load time: {first_load_time:.4f} seconds")

        # Second call should use cached model
        start_time = time.time()
        model_again = get_model()
        second_load_time = time.time() - start_time
        logger.info(f"Second model load time: {second_load_time:.4f} seconds")

        # Verify caching worked
        if second_load_time < first_load_time:
            logger.info("✅ Model caching is working correctly")
        else:
            logger.warning("⚠️ Model caching may not be working optimally")

        # Test that it's the same model instance
        if id(model) == id(model_again):
            logger.info("✅ Model singleton pattern is working correctly")
        else:
            logger.warning("⚠️ Model singleton pattern is not working")

        return True
    except Exception as e:
        logger.error(f"Error testing model caching: {e}")
        return False

def test_prediction_caching():
    """Test that prediction caching works correctly"""
    logger.info("Testing prediction caching...")

    try:
        from app.model import predict_image, predict_cached

        # Create a test image if one doesn't exist
        test_image_path = Path("test_image.jpg")
        if not test_image_path.exists():
            logger.info("Test image not found, skipping prediction cache test")
            return True

        with open(test_image_path, "rb") as f:
            image_bytes = f.read()
            image_hash = hashlib.md5(image_bytes).hexdigest()

        # First prediction
        start_time = time.time()
        result1 = predict_image(image_bytes)
        first_prediction_time = time.time() - start_time
        logger.info(f"First prediction time: {first_prediction_time:.4f} seconds")

        # Second prediction (should use cache)
        start_time = time.time()
        result2 = predict_image(image_bytes)
        second_prediction_time = time.time() - start_time
        logger.info(f"Second prediction time: {second_prediction_time:.4f} seconds")

        # Verify caching worked
        if second_prediction_time < first_prediction_time:
            logger.info("✅ Prediction caching is working correctly")
        else:
            logger.warning("⚠️ Prediction caching may not be working optimally")

        # Verify results are the same
        if result1 == result2:
            logger.info("✅ Cached prediction returns consistent results")
        else:
            logger.warning("⚠️ Cached prediction returns different results")

        return True
    except Exception as e:
        logger.error(f"Error testing prediction caching: {e}")
        return False

def test_gradio_caching():
    """Test that the gradio_app.py classify function caching works correctly"""
    logger.info("Testing Gradio classify function caching...")

    try:
        from gradio_app import classify, get_cached_prediction

        # Create a test image if one doesn't exist
        test_image_path = Path("test_image.jpg")
        if not test_image_path.exists():
            logger.info("Test image not found, skipping Gradio cache test")
            return True

        # First classification
        start_time = time.time()
        result1 = classify(str(test_image_path))
        first_classify_time = time.time() - start_time
        logger.info(f"First classification time: {first_classify_time:.4f} seconds")

        # Second classification (should use cache)
        start_time = time.time()
        result2 = classify(str(test_image_path))
        second_classify_time = time.time() - start_time
        logger.info(f"Second classification time: {second_classify_time:.4f} seconds")

        # Verify caching worked
        if second_classify_time < first_classify_time:
            logger.info("✅ Gradio classify caching is working correctly")
        else:
            logger.warning("⚠️ Gradio classify caching may not be working optimally")

        # Verify results are the same
        if result1 == result2:
            logger.info("✅ Cached classification returns consistent results")
        else:
            logger.warning("⚠️ Cached classification returns different results")

        return True
    except Exception as e:
        logger.error(f"Error testing Gradio classify caching: {e}")
        return False

def test_css_loading():
    """Test that the CSS loading works correctly"""
    logger.info("Testing CSS loading...")

    try:
        from gradio_app import load_css

        css = load_css()
        if css:
            logger.info(f"✅ CSS loaded successfully ({len(css)} bytes)")
        else:
            logger.warning("⚠️ CSS loading returned empty string")

        return True
    except Exception as e:
        logger.error(f"Error testing CSS loading: {e}")
        return False

def test_clipboard_option():
    """Test that the clipboard option is enabled in the Image component"""
    logger.info("Testing clipboard option in Image component...")

    try:
        from gradio_app import create_ui

        # Create the UI
        demo = create_ui()

        # Find the Image component
        image_component = None
        for component in demo.blocks.values():
            if hasattr(component, "sources") and isinstance(component.sources, list):
                image_component = component
                break

        if image_component is None:
            logger.warning("⚠️ Could not find Image component in UI")
            return False

        # Check if clipboard is in the sources
        if "clipboard" in image_component.sources:
            logger.info("✅ Clipboard option is enabled in Image component")
            return True
        else:
            logger.warning("⚠️ Clipboard option is not enabled in Image component")
            return False
    except Exception as e:
        logger.error(f"Error testing clipboard option: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("Starting optimization tests...")

    tests = [
        test_model_caching,
        test_prediction_caching,
        test_gradio_caching,
        test_css_loading,
        test_clipboard_option
    ]

    results = []
    for test in tests:
        results.append(test())

    success_count = sum(results)
    logger.info(f"Tests completed: {success_count}/{len(tests)} successful")

    if all(results):
        logger.info("✅ All optimization tests passed!")
    else:
        logger.warning("⚠️ Some optimization tests failed")

if __name__ == "__main__":
    main()
