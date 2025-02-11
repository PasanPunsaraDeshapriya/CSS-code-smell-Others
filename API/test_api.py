import requests

# URL of the API endpoint (update to your running server address)
url = 'http://127.0.0.1:5000/predict'  # For local testing
# url = 'http://192.168.8.145:5000/predict'  # For testing on the network

# Example CSS code to send for prediction
css_code = """
body {
    background-color: #fff;
    color: #333;
}
#main-content {
    margin: 0 auto;
    width: 80%;
}
"""

# Send a POST request to the API
response = requests.post(url, json={'css_code': css_code})

# Output the result
if response.status_code == 200:
    print("Predicted Class:", response.json()['predicted_class'])
else:
    print("Error:", response.status_code, response.text)
