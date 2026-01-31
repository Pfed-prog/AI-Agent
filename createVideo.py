import requests
import json

url = "https://api.d-id.com/talks"

headers = {
    "accept": "application/json",
    "authorization": "Basic Wm1Wa2IzSnZkbTR4T1VCbmJXRnBiQzVqYjIwOjh1NVI4bmRNQ1A1dm9ydjhmUWZJXw==",
    "content-type": "application/json",
}

data = {
    "script": {
        "type": "text",
        "provider": {
            "type": "elevenlabs", "voice_id": "21m00Tcm4TlvDq8ikWAM"
            },
        "input": "Hello, this is a new video"
    },
    "source_url": "https://i.postimg.cc/TYsYbY6v/Day-1-the-phope-kidduuuu-848-resized-(1).jpg"
}

response = requests.post(url, headers=headers, json=data)
output = response.content

print(output)
#b'{"id":"tlk_XzjIOL70HTOJuNp5nHvKu","created_at":"2026-01-31T18:45:45.905Z","created_by":"google-oauth2|110628693356570030047","status":"created","object":"talk"}'