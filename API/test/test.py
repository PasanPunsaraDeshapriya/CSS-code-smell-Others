import requests

# Define the API endpoint
url = "http://localhost:5000/predict"

# Define the CSS code to test
css_code = """
body { color: red; }
.class { font-size: 12px; }
#id { margin: 0; }
"""

# Create the payload
payload = {
    "css_code": css_code
}

# Send the POST request
response = requests.post(url, json=payload)

# Print the response
if response.status_code == 200:
    print("✅ Prediction successful!")
    print(response.json())
else:
    print(f"❌ Error: {response.status_code}")
    print(response.json())