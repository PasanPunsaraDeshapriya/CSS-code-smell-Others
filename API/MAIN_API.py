from flask import Flask, request, jsonify
import joblib
import re
import os
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Load the trained model

# MODEL_PATH = r"d:\IIT 4th year\FYP\Creation\API\new api\css_smell_predictor_all_4.pkl"
MODEL_PATH = r"D:\Documents\IIT\FYP\CSS-code-smell-Others\API\Main API\css_smell_predictor_all_4.pkl"

clf = joblib.load(MODEL_PATH)

# Feature extraction function
# def extract_features_from_css(css_code):
#     """
#     Extracts features from CSS to match the trained model input.
#     Returns a dictionary of extracted features.
#     """
#     features = {
#         "nesting_depth": css_code.count('{') - css_code.count('}'),
#         "num_ids": css_code.count('#'),
#         "num_classes": css_code.count('.'),
#         "num_important": css_code.count('!important'),
#         "duplicate_selectors": len(re.findall(r'([^\{\}]+)\s*\{', css_code)) - len(set(re.findall(r'([^\{\}]+)\s*\{', css_code))),
#         "total_rules": css_code.count('}'),
#         "deep_nesting": max([line.count('{') for line in css_code.split('\n') if '{' in line] + [0]),
#         "long_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if len(selector) > 50),
#         "overqualified_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if 'html' in selector or 'body' in selector),
#         "browser_specific_properties": sum(1 for prop in re.findall(r'-(moz|webkit|ms|o)-', css_code)),
#         "total_properties": css_code.count(';'),
#         "avg_properties_per_rule": css_code.count(';') / (css_code.count('}') + 1),
#         "inline_styles": css_code.count('style='),
#         "unused_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if len(selector.split()) > 3),
#         "universal_selectors": css_code.count('*'),
#         "excessive_specificity": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if selector.count(' ') > 3),
#         "vendor_prefixes": sum(1 for _ in re.findall(r'-(webkit|moz|ms|o)-', css_code)),
#         "animation_usage": css_code.count('@keyframes'),
#         "excessive_zindex": sum(1 for prop in re.findall(r'z-index\s*:\s*(\d+)', css_code) if int(prop) > 10),
#         "unused_media_queries": sum(1 for mq in re.findall(r'@media\s*\((.*?)\)', css_code) if 'print' in mq or 'speech' in mq),
#         "color_hex_usage": css_code.count('#'),
#         "excessive_font_sizes": sum(1 for prop in re.findall(r'font-size\s*:\s*(\d+)', css_code) if int(prop) > 40)
#     }
    
#     return list(features.values()), features  # Return both list (for model) and dict (for visualization)

# def extract_features_from_css(css_code):
#     """
#     Extracts features from CSS and prints their count for debugging.
#     """
#     features = {
#         "nesting_depth": css_code.count('{') - css_code.count('}'),
#         "num_ids": css_code.count('#'),
#         "num_classes": css_code.count('.'),
#         "num_important": css_code.count('!important'),
#         "duplicate_selectors": len(re.findall(r'([^\{\}]+)\s*\{', css_code)) - len(set(re.findall(r'([^\{\}]+)\s*\{', css_code))),
#         "total_rules": css_code.count('}'),
#         "deep_nesting": max([line.count('{') for line in css_code.split('\n') if '{' in line] + [0]),
#         "long_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if len(selector) > 50),
#         "overqualified_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if 'html' in selector or 'body' in selector),
#         "browser_specific_properties": sum(1 for prop in re.findall(r'-(moz|webkit|ms|o)-', css_code)),
#         "total_properties": css_code.count(';'),
#         "avg_properties_per_rule": css_code.count(';') / (css_code.count('}') + 1),
#         "inline_styles": css_code.count('style='),
#         "unused_selectors": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if len(selector.split()) > 3),
#         "universal_selectors": css_code.count('*'),
#         "excessive_specificity": sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if selector.count(' ') > 3),
#         "vendor_prefixes": sum(1 for _ in re.findall(r'-(webkit|moz|ms|o)-', css_code)),
#         "animation_usage": css_code.count('@keyframes'),
#         "excessive_zindex": sum(1 for prop in re.findall(r'z-index\s*:\s*(\d+)', css_code) if int(prop) > 10),
#         "unused_media_queries": sum(1 for mq in re.findall(r'@media\s*\((.*?)\)', css_code) if 'print' in mq or 'speech' in mq),
#         "color_hex_usage": css_code.count('#'),
#         "excessive_font_sizes": sum(1 for prop in re.findall(r'font-size\s*:\s*(\d+)', css_code) if int(prop) > 40)
#     }

#     # print(f"✅ Extracted Features ({len(features)} total): {list(features.keys())}")
#     # print(f"✅ Feature Values: {list(features.values())}")
#     # # Check what features the model expects
#     # print("Model trained with features:", clf.feature_names_in_)

    
#     # return list(features.values()), features  # Return list (for model) and dict (for debugging)

def extract_features_from_css(css_code):
    """
    Extracts features from CSS and prints their count for debugging.
    """
    if not css_code.strip():
        return [], {}  # Return empty list and dictionary if no CSS code is given

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


# @app.route('/predict', methods=['POST'])
# def predict():
#     """
#     API endpoint to receive CSS code and return predictions.
#     """
#     data = request.json
#     css_code = data.get("css_code", "")

#     if not css_code:
#         return jsonify({"error": "No CSS code provided"}), 400

#     feature_list, feature_dict = extract_features_from_css(css_code)

#     # Get prediction
#     # prediction = clf.predict([feature_list])[0]


#     # Ensure the feature names match what the model expects
#     feature_names = [
#         "nesting_depth", "num_ids", "num_classes", "num_important", "duplicate_selectors",
#         "total_rules", "deep_nesting", "long_selectors", "overqualified_selectors", 
#         "browser_specific_properties", "total_properties", "avg_properties_per_rule",
#         "inline_styles", "unused_selectors", "universal_selectors", "excessive_specificity",
#         "vendor_prefixes", "animation_usage", "excessive_zindex", "unused_media_queries",
#         "color_hex_usage", "excessive_font_sizes"
#     ]

#     # Convert the feature list into a DataFrame with correct feature names
#     feature_df = pd.DataFrame([feature_list], columns=feature_names)

#     # Make the prediction using the correctly formatted DataFrame
#     prediction = clf.predict(feature_df)[0]


#     return jsonify({
#         "prediction": prediction,
#         "features": feature_dict
#     })

# @app.route('/predict', methods=['POST'])
# def predict():
#     """
#     API endpoint to receive CSS code and return predictions.
#     """
#     data = request.json
#     css_code = data.get("css_code", "")

#     if not css_code:
#         return jsonify({"error": "No CSS code provided"}), 400

#     feature_list, feature_dict = extract_features_from_css(css_code)

#     if not feature_list:
#         return jsonify({"error": "Feature extraction failed. No valid features found."}), 400

#     # Ensure the feature names match what the model expects
#     feature_names = [
#         "nesting_depth", "num_ids", "num_classes", "num_important", "duplicate_selectors",
#         "total_rules", "deep_nesting", "long_selectors", "overqualified_selectors", 
#         "browser_specific_properties", "total_properties", "avg_properties_per_rule",
#         "inline_styles", "unused_selectors", "universal_selectors", "excessive_specificity",
#         "vendor_prefixes", "animation_usage", "excessive_zindex", "unused_media_queries",
#         "color_hex_usage", "excessive_font_sizes"
#     ]

#     # Convert the feature list into a DataFrame with correct feature names
#     try:
#         feature_df = pd.DataFrame([feature_list], columns=feature_names)
#         prediction = clf.predict(feature_df)[0]
#     except Exception as e:
#         return jsonify({"error": f"Prediction error: {str(e)}"}), 500

#     return jsonify({
#         "prediction": prediction,
#         "features": feature_dict
#     })

@app.route('/predict', methods=['POST'])
def predict():
    """
    API endpoint to receive CSS code and return predictions.
    """
    data = request.json
    css_code = data.get("css_code", "")

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

        prediction = clf.predict(feature_df)[0]

        # Create a smells dictionary based on feature values
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
