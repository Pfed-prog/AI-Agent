import requests
import json

url = "https://api.d-id.com/talks"

headers = {
    "accept": "application/json",
    "authorization": "Basic Wm1Wa2IzSnZkbTR4T1VCbmJXRnBiQzVqYjIwOjh1NVI4bmRNQ1A1dm9ydjhmUWZJXw==",
}

response = requests.get(url, headers=headers)
data = response.content


# Step 1: Decode the byte string into a regular string
decoded_data = data.decode('utf-8')

# Step 2: Load the JSON data
json_data = json.loads(decoded_data)

# Step 3: Access the 'result_url' field
#data = json_data['talks'][0]['result_url']

fields = len(json_data['talks'])
print(fields)