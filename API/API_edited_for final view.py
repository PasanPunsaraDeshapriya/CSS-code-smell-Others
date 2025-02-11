from flask import Flask, request, jsonify
# Flask: Creates the RESTful API.
# request: Handles incoming data (e.g., CSS code sent by the user).
# jsonify: Converts Python dictionaries into JSON format for the API response.

import joblib
# joblib: Loads the pre-trained ML model (css_smell_predictor_all.pkl).

import re
# re: Regular expressions for pattern matching in CSS code (e.g., selectors, properties).

import os
import pandas as pd
# pandas: Structures data in tabular format (DataFrame) for model input.

from flask_cors import CORS
# CORS: Enables Cross-Origin Resource Sharing, allowing the API to be accessed from different domains (like front-end apps).

app = Flask(__name__)
CORS(app)
# Allows cross-origin requests, enabling front-end applications to call the API without security issues.

# Load the trained model
MODEL_PATH = r"d:\IIT 4th year\FYP\Creation\API\new api\css_smell_predictor_all.pkl"
clf = joblib.load(MODEL_PATH)

def extract_features_from_css(css_code):
    # This function analyzes the CSS code and extracts specific features (metrics) relevant for code smell detection.
    """
    Extracts features from CSS and prints their count for debugging.
    """
    if not css_code.strip():
        return [], {}  # Return empty list and dictionary if no CSS code is given

    features = {
        "nesting_depth": css_code.count('{') - css_code.count('}'),
        # nesting_depth: Measures how deeply CSS rules are nested ({}).

        "num_ids": css_code.count('#'),
        # num_ids: Counts the number of # (ID selectors).

        "num_classes": css_code.count('.'),
        # num_classes: Counts the number of . (class selectors).

        "num_important": css_code.count('!important'),
        # num_important: Counts occurrences of !important (often a sign of poor CSS practice).

        "duplicate_selectors": len(re.findall(r'([^\{\}]+)\s*\{', css_code)) - len(set(re.findall(r'([^\{\}]+)\s*\{', css_code))),
        # duplicate_selectors: Detects repeated selectors using regular expressions.

        "total_rules": css_code.count('}'),
        # total_rules: Counts total CSS rules (based on }).

        "deep_nesting": max([line.count('{') for line in css_code.split('\n') if '{' in line] + [0]),
        # deep_nesting: Measures the deepest level of nesting in the CSS.

        "long_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if len(selector) > 50),
        # long_selectors: Counts selectors longer than 50 characters (overly complex selectors).

        "overqualified_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if 'html' in selector or 'body' in selector),
        # overqualified_selectors: Detects selectors unnecessarily qualified with html or body.

        "browser_specific_properties": sum(1 for prop in re.findall(r'-(moz|webkit|ms|o)-', css_code)),
        # browser_specific_properties: Checks for vendor-specific prefixes (-webkit-, -moz-).
        
        "total_properties": css_code.count(';'),
        # Counts the total number of CSS properties in the code.

        "avg_properties_per_rule": css_code.count(';') / (css_code.count('}') + 1) if css_code.count('}') > 0 else 0,
        # Calculates the average number of CSS properties per rule.

        "inline_styles": css_code.count('style='),
        # Counts occurrences of inline styles in the CSS code.

        "unused_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if len(selector.split()) > 3),
        # Counts CSS selectors that are potentially too complex or likely unused.

        "universal_selectors": css_code.count('*'),
        # Counts the number of universal selectors (*) used in the CSS code.

        "excessive_specificity": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if selector.count(' ') > 3),
        # Counts CSS selectors with excessive specificity.

        "vendor_prefixes": sum(1 for _ in re.findall(r'-(webkit|moz|ms|o)-', css_code)),
        # Counts the number of vendor-prefixed properties. like webkit, moz, ms, o......

        "animation_usage": css_code.count('@keyframes'),
        # animation_usage: Counts occurrences of @keyframes.

        "excessive_zindex": sum(1 for prop in re.findall(r'z-index\s*:\s*(\d+)', css_code) if int(prop) > 10),
        # excessive_zindex: Detects unusually high z-index values (greater than 10).

        "unused_media_queries": sum(1 for mq in re.findall(r'@media\s*\((.*?)\)', css_code) if 'print' in mq or 'speech' in mq),
        #  Counts the number of potentially unused media queries, specifically targeting print and speech media types.

        "color_hex_usage": css_code.count('#'),
        # Counts the number of hex color codes used in the CSS code.

        "excessive_font_sizes": sum(1 for prop in re.findall(r'font-size\s*:\s*(\d+)', css_code) if int(prop) > 40)
        # excessive_font_sizes: Detects font-size values greater than 40 (possibly inconsistent design).

    }

    return list(features.values()), features
    # returns the list of feature values

@app.route('/predict', methods=['POST'])
def predict():
    # This is the API URL that external applications will call to get CSS code smell predictions.
    """
    API endpoint to receive CSS code and return predictions.
    """
    data = request.json
    css_code = data.get("css_code", "")
    # Extracts the CSS code from the JSON payload

    if not css_code:
        return jsonify({"error": "No CSS code provided", "features": {}, "smells": {}}), 400

    try:
        feature_list, feature_dict = extract_features_from_css(css_code)

        if feature_list is None or feature_dict is None:
            return jsonify({"error": "Feature extraction failed", "features": {}, "smells": {}}), 500

        # Convert features into DataFrame
        feature_df = pd.DataFrame([feature_list], columns=[
            "nesting_depth", "num_ids", "num_classes", "num_important", 
            "duplicate_selectors", "total_rules", "deep_nesting", "long_selectors", 
            "overqualified_selectors", "browser_specific_properties", "total_properties", 
            "avg_properties_per_rule", "inline_styles", "unused_selectors", "universal_selectors", 
            "excessive_specificity", "vendor_prefixes", "animation_usage", "excessive_zindex", 
            "unused_media_queries", "color_hex_usage", "excessive_font_sizes"
        ])
        # Converts the feature list into a Pandas DataFrame because machine learning models in Python usually accept DataFrames as input.

        prediction = clf.predict(feature_df)[0]
        # Uses the loaded model to predict if the provided CSS code contains code smells.

        # Create a smells dictionary based on filters features to include only those with problematic values (e.g., high z-index, deep nesting).
        smells = {key: value for key, value in feature_dict.items() if value > 0}

        response_data = {
            "prediction": prediction,
            "features": feature_dict if feature_dict else {},  # Ensure features is not None
            "smells": smells if smells else {}  # Ensure smells is not None
        }

        print("✅ API Response:", response_data)  # Debugging log

        return jsonify(response_data)

    except Exception as e:
        print(f"❌ Error in API: {str(e)}")
        return jsonify({"error": "Internal Server Error", "features": {}, "smells": {}, "details": str(e)}), 500
# Catches any unexpected errors during processing and returns an appropriate error message.

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
