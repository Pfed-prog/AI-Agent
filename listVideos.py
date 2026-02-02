import requests
import json

url = "https://api.d-id.com/talks"

headers = {
    "accept": "application/json",
    "authorization": "Basic Y0c5emRHRnNabVZrYjNSdmRrQm5iV0ZwYkM1amIyMDpjajR0THg2MHVYYmhjOEtpUVBEVFI=",
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

data = json_data['talks'][0]['result_url']
print(data)