import requests

url = "http://localhost:5000/chat"
headers = {"Content-Type": "application/json"}
data = {
    "message": "show me candles under 300"
}

response = requests.post(url, json=data)

print("Raw response:")
print(response.text)  # show raw HTML or JSON response
