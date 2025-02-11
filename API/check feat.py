import joblib

# Load the model
model_path = "css_smell_predictor_3.pkl"
clf = joblib.load(model_path)

# Print expected feature count
print(f"✅ Model expects {clf.n_features_in_} features.")
