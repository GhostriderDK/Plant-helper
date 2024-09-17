import requests

# The public IP address of your Raspberry Pi
url = "http://<YOUR_RASPBERRY_PI_PUBLIC_IP>:5000/receive"

# Data to be sent to the Flask app
data = {"message": "Hello from PythonAnywhere!"}

# Send a POST request to the Flask app on Raspberry Pi
response = requests.post(url, json=data)

# Print the response from the Flask app
print(response.status_code)
print(response.json())
