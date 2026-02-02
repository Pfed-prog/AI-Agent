import requests
import json

url = "https://api.d-id.com/talks"

headers = {
    "accept": "application/json",
    "authorization": "Basic Wm1Wa2IzSnZkbTR4T1VCbmJXRnBiQzVqYjIwOjFXNm80NW0wQ29CS213WEtLcUIxUg==",
    "content-type": "application/json",
}

data = {
    "script": {
        "type": "text",
        "provider": {
            "type": "elevenlabs", "voice_id": "EXAVITQu4vr4xnSDxMaL"
            },
        "input": "Понятно. Начнем с первой популярной теории — теории накопления ошибок в ДНК. Вроде бы неплохо звучит, но где доказательства того, что именно мутации являются причиной старения, а не просто следствием других процессов в клетке? Какие есть ключевые исследования, подтверждающие эту связь?"
    },
    "source_url": "https://i.postimg.cc/R0hsHj2X/pexels-photo-19248758.jpg"
}

response = requests.post(url, headers=headers, json=data)
output = response.content

print(output)
#b'{"id":"tlk_XzjIOL70HTOJuNp5nHvKu","created_at":"2026-01-31T18:45:45.905Z","created_by":"google-oauth2|110628693356570030047","status":"created","object":"talk"}'