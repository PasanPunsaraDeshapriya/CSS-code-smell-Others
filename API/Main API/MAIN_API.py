from flask import Flask, request, jsonify
import joblib
import re
import pandas as pd
from flask_cors import CORS
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the trained model
MODEL_PATH = r"D:\Documents\IIT\FYP\CSS-code-smell-Others\API\Main API\css_smell_predictor_all_4.pkl"
try:
    clf = joblib.load(MODEL_PATH)
    logger.info("✅ Model loaded successfully.")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")
    clf = None

# Feature extraction function
def extract_features_from_css(css_code):
    """
    Extracts features from CSS code and returns a list of feature values and a dictionary of features.
    """
    if not css_code or not css_code.strip():
        return [], {}

    features = {
        "nesting_depth": css_code.count('{') - css_code.count('}'),
        "num_ids": css_code.count('#'),
        "num_classes": css_code.count('.'),
        "num_important": css_code.count('!important'),
        "duplicate_selectors": len(re.findall(r'([^\{\}]+)\s*\{', css_code)) - len(set(re.findall(r'([^\{\}]+)\s*\{', css_code))),
        "total_rules": css_code.count('}'),
        "deep_nesting": max([line.count('{') for line in css_code.split('\n') if '{' in line] + [0]),
        "long_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if len(selector) > 50),
        "overqualified_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if 'html' in selector or 'body' in selector),
        "browser_specific_properties": sum(1 for prop in re.findall(r'-(moz|webkit|ms|o)-', css_code)),
        "total_properties": css_code.count(';'),
        "avg_properties_per_rule": css_code.count(';') / (css_code.count('}') + 1) if css_code.count('}') > 0 else 0,
        "inline_styles": css_code.count('style='),
        "unused_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if len(selector.split()) > 3),
        "universal_selectors": css_code.count('*'),
        "excessive_specificity": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if selector.count(' ') > 3),
        "vendor_prefixes": sum(1 for _ in re.findall(r'-(webkit|moz|ms|o)-', css_code)),
        "animation_usage": css_code.count('@keyframes'),
        "excessive_zindex": sum(1 for prop in re.findall(r'z-index\s*:\s*(\d+)', css_code) if int(prop) > 10),
        "unused_media_queries": sum(1 for mq in re.findall(r'@media\s*\((.*?)\)', css_code) if 'print' in mq or 'speech' in mq),
        "color_hex_usage": css_code.count('#'),
        "excessive_font_sizes": sum(1 for prop in re.findall(r'font-size\s*:\s*(\d+)', css_code) if int(prop) > 40)
    }

    return list(features.values()), features

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    """
    API endpoint to receive CSS code and return predictions.
    """
    try:
        data = request.json
        css_code = data.get("css_code", "")

        if not css_code or not css_code.strip():
            logger.warning("❌ No CSS code provided in request.")
            return jsonify({"error": "No CSS code provided", "features": {}, "smells": {}}), 400

        # Extract features
        feature_list, feature_dict = extract_features_from_css(css_code)
        if not feature_list or not feature_dict:
            logger.error("❌ Feature extraction failed.")
            return jsonify({"error": "Feature extraction failed", "features": {}, "smells": {}}), 500

        # Ensure the model is loaded
        if not clf:
            logger.error("❌ Model not loaded.")
            return jsonify({"error": "Model not loaded", "features": {}, "smells": {}}), 500

        # Convert features into DataFrame
        feature_df = pd.DataFrame([feature_list], columns=[
            "nesting_depth", "num_ids", "num_classes", "num_important", 
            "duplicate_selectors", "total_rules", "deep_nesting", "long_selectors", 
            "overqualified_selectors", "browser_specific_properties", "total_properties", 
            "avg_properties_per_rule", "inline_styles", "unused_selectors", "universal_selectors", 
            "excessive_specificity", "vendor_prefixes", "animation_usage", "excessive_zindex", 
            "unused_media_queries", "color_hex_usage", "excessive_font_sizes"
        ])

        # Make prediction
        prediction = clf.predict(feature_df)[0]

        # Create a smells dictionary based on feature values
        smells = {key: value for key, value in feature_dict.items() if value > 0}

        # Prepare response
        response_data = {
            "prediction": prediction,
            "features": feature_dict,
            "smells": smells
        }

        logger.info("✅ Prediction successful.")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"❌ Error in /predict endpoint: {e}")
        return jsonify({"error": "Internal Server Error", "features": {}, "smells": {}, "details": str(e)}), 500

# Health check endpoint
@app.route('/')
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return "CSS Smell Detector API is running!"

# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)