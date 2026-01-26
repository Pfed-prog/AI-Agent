from dotenv import load_dotenv
import os

import openai
from elevenlabs.client import ElevenLabs
import requests
import time
import json

# Конфигурация API-ключей
openai.api_key = "YOUR_OPENAI_KEY"
D_ID_API_KEY = "YOUR_D_ID_KEY"

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

# Конфигурация агентов
agents = {
    "alexis": {
        "name": "Алексис",
        "system_prompt": "Ты скептичный биоинформатик. Ты задаешь острые вопросы и требуешь ссылки на исследования. Говори кратко.",
        "voice_id": "EXAVITQu4vr4xnSDxMaL", # ID голоса из ElevenLabs
        "avatar_image_url": "https://.../alexis.png",
        "d_id_source_url": "D_ID_SOURCE_ID_FOR_ALEXIS" # ID созданного в D-ID "source"
    },
    "ben": {
        "name": "Бен",
        "system_prompt": "Ты оптимистичный геронтолог, энтузиаст исследований долголетия. Говори увлеченно.",
        "voice_id": "JBFqnCBsd6RMkjVDRZzb", # Другой голос
        "avatar_image_url": "https://.../ben.png",
        "d_id_source_url": "D_ID_SOURCE_ID_FOR_BEN"
    }
}

# Начало диалога
topic = "Обсудим основные современные теории старения."
history = [{"role": "system", "content": f"Тема дискуссии: {topic}. Вы ведете научный, но живой диалог."}]
current_speaker = "alexis"
next_speaker = "ben"

def generate_reply(agent_name, dialog_history):
    """Генерирует текст реплики для агента."""
    agent = agents[agent_name]
    messages = dialog_history + [{"role": "system", "content": agent["system_prompt"]}]
    # Запрашиваем у LLM ответ от лица агента
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=150
    )
    reply_text = response.choices[0].message.content
    print(f"{agent['name']}: {reply_text}")
    return reply_text

def generate_speech(text, output_filename):
    """Создает аудиофайл из текста."""
    audio = elevenlabs.text_to_speech.convert(
        text="The first move is what sets everything in motion.",
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    with open(output_filename, 'wb') as f:
        f.write(audio)
    return output_filename

def create_avatar_video(audio_filename, agent_name, output_filename):
    """Отправляет аудио и фото аватара в D-ID, создает видео."""
    agent = agents[agent_name]
    url = "https://api.d-id.com/talks"
    payload = {
        "source_url": agent["d_id_source_url"],
        "script": {
            "type": "audio",
            "audio_url": f"file://{audio_filename}" # В реальности нужно загрузить на сервер
        }
    }
    headers = {
        "Authorization": f"Bearer {D_ID_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    talk_id = response.json()['id']
    # Ожидание завершения рендера и загрузка видео...
    # (Здесь нужен дополнительный код для проверки статуса и скачивания)
    return output_filename # Путь к итоговому видео

# Главный цикл диалога (3 обмена репликами для примера)
for i in range(3):
    print(f"\n--- Ход {i+1} ---")
    
    # 1. Генерация текста
    reply_text = generate_reply(current_speaker, history)
    history.append({"role": "user", "content": reply_text})
    
    # 2. Генерация аудио
    audio_file = f"turn_{i}_{current_speaker}.mp3"
    generate_speech(reply_text, agents[current_speaker]["voice_id"], audio_file)
    
    # 3. Генерация видео с аватаром
    video_file = f"turn_{i}_{current_speaker}.mp4"
    create_avatar_video(audio_file, current_speaker, video_file)
    
    # 4. ЗАГЛУШКА: Здесь код, который добавляет video_file в OBS для воспроизведения
    print(f"[OBS] Воспроизводится: {video_file}")
    # Например, используя obsws-python (WebSocket плагин для OBS)
    
    # Пауза, соответствующая длине видео
    time.sleep(10) # Примерная длительность
    
    # Меняем говорящего
    current_speaker, next_speaker = next_speaker, current_speaker

print("\n--- Дискуссия завершена ---")