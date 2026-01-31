import requests
import json

url = "https://api.d-id.com/talks/tlk_XzjIOL70HTOJuNp5nHvKu"

headers = {
    "accept": "application/json",
    "authorization": "Basic Wm1Wa2IzSnZkbTR4T1VCbmJXRnBiQzVqYjIwOjh1NVI4bmRNQ1A1dm9ydjhmUWZJXw==",
}

response = requests.get(url, headers=headers)
data = response.content
print(data)

# Step 1: Decode the byte string into a regular string
decoded_data = data.decode('utf-8')

# Step 2: Load the JSON data
json_data = json.loads(decoded_data)

# Step 3: Access the 'result_url' field
result_url = json_data['result_url']

# Step 4: Print or use the result_url
print(result_url)
response = requests.get(result_url)
print(response)
# Save the video to a file
with open('video.mp4', 'wb') as f:
    f.write(response.content)
print("Video downloaded successfully.")
