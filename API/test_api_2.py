from flask import Flask, request, jsonify
import joblib
import re

# Load the trained model
model_path = "css_smell_classifier.pkl"  # Ensure this file is in the same directory
clf = joblib.load(model_path)

# Create Flask app
app = Flask(__name__)

# Feature extraction function
def extract_features(css_code):
    nesting_depth = css_code.count('{') - css_code.count('}')
    num_ids = css_code.count('#')
    num_classes = css_code.count('.')
    num_important = css_code.count('!important')
    selectors = re.findall(r'([^\{\}]+)\s*\{', css_code)
    duplicate_selectors = len(selectors) - len(set(selectors))
    return [nesting_depth, num_ids, num_classes, num_important, duplicate_selectors]

# API endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    css_code = data.get("css_code", "")
    features = extract_features(css_code)
    prediction = clf.predict([features])[0]
    return jsonify({"predicted_class": prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
