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

# Paths
MODEL_PATH = r"D:\Documents\IIT\FYP\CSS-code-smell-Others\API\test\css_smell_model_with_clustering.pkl"
SCALER_PATH = r"D:\Documents\IIT\FYP\CSS-code-smell-Others\API\test\scaler.pkl"
CLUSTER_MODEL_PATH = r"D:\Documents\IIT\FYP\CSS-code-smell-Others\API\test\kmeans.pkl"

# Load models
try:
    clf = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    kmeans = joblib.load(CLUSTER_MODEL_PATH)
    logger.info("✅ Models loaded successfully.")
except Exception as e:
    logger.error(f"❌ Error loading models: {e}")
    clf, scaler, kmeans = None, None, None

# Feature extraction function
def extract_features_from_css(css_code):
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
    try:
        data = request.json
        css_code = data.get("css_code", "")

        if not css_code or not css_code.strip():
            return jsonify({"error": "No CSS code provided", "features": {}, "smells": {}}), 400

        feature_list, feature_dict = extract_features_from_css(css_code)

        if not feature_list or not feature_dict:
            return jsonify({"error": "Feature extraction failed", "features": {}, "smells": {}}), 500

        if not clf or not scaler or not kmeans:
            return jsonify({"error": "Model(s) not loaded", "features": {}, "smells": {}}), 500

        feature_names = [
            "nesting_depth", "num_ids", "num_classes", "num_important", 
            "duplicate_selectors", "total_rules", "deep_nesting", "long_selectors", 
            "overqualified_selectors", "browser_specific_properties", "total_properties", 
            "avg_properties_per_rule", "inline_styles", "unused_selectors", "universal_selectors", 
            "excessive_specificity", "vendor_prefixes", "animation_usage", "excessive_zindex", 
            "unused_media_queries", "color_hex_usage", "excessive_font_sizes"
        ]

        feature_df = pd.DataFrame([feature_list], columns=feature_names)
        scaled_features = scaler.transform(feature_df)

        prediction = clf.predict(scaled_features)[0]
        cluster = kmeans.predict(scaled_features)[0]

        severity_map = {0: "Clean", 1: "Low", 2: "Medium", 3: "High"}
        severity_label = severity_map.get(cluster, "Unknown")

        smells = {k: v for k, v in feature_dict.items() if v > 0}

        return jsonify({
            "prediction": round(float(prediction), 2),
            "severity_label": severity_label,
            "features": feature_dict,
            "smells": smells
        })

    except Exception as e:
        logger.error(f"❌ Error in /predict: {e}")
        return jsonify({"error": "Internal Server Error", "features": {}, "smells": {}, "details": str(e)}), 500

# Health check
@app.route('/')
def health_check():
    return "CSS Smell Detector API is running!"

# Run server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
