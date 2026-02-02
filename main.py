import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer

from dotenv import load_dotenv
import os

from openai import OpenAI
import time
import json

# Конфигурация API-ключей
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
D_ID_API_KEY = os.getenv("D_ID_API_KEY")

client = OpenAI()

# Конфигурация агентов
agents = {
    "alexis": {
        "name": "Алексис",
        "system_prompt": "Ты скептичный биоинформатик. Ты задаешь острые вопросы и требуешь ссылки на исследования. Говори кратко.",
        "voice_id": "EXAVITQu4vr4xnSDxMaL", # ID голоса из ElevenLabs
        "avatar_image_url": "https://i.postimg.cc/R0hsHj2X/pexels-photo-19248758.jpg",
    },
    "ben": {
        "name": "Бен",
        "system_prompt": "Ты оптимистичный геронтолог, энтузиаст исследований долголетия. Говори увлеченно.",
        "voice_id": "JBFqnCBsd6RMkjVDRZzb", # Другой голос
        "avatar_image_url": "https://i.postimg.cc/3JkPs0tC/pexels-photo-16886377.jpg",
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
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=150
    )
    reply_text = response.choices[0].message.content
    print(f"{agent['name']}: {reply_text}")
    print(f"character length: {len(reply_text)}")
    return reply_text

def create_avatar_video(agent_name, reply_text):
    """Отправляет аудио и фото аватара в D-ID, создает видео."""
    agent = agents[agent_name]
    url = "https://api.d-id.com/talks"
    payload = {
        "script": {
            "type": "text",
            "provider": {
                "type": "elevenlabs", "voice_id": agent['voice_id']
                },
            "input": reply_text
        },
        "source_url": agent['avatar_image_url']
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Basic {D_ID_API_KEY}",
        "content-type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    
    data = response.content
    print(data)
    decoded_data = data.decode('utf-8')
    json_data = json.loads(decoded_data)
    talk_id = json_data['id']

    return talk_id

""" def get_video_url(talk_id):

    headers = {
        "accept": "application/json",
        "Authorization": f"Basic {D_ID_API_KEY}",
    }
    url = f"https://api.d-id.com/talks/{talk_id}"
    response = requests.get(url, headers=headers)
    data = response.content

    print(data)
    # Step 1: Decode the byte string into a regular string
    decoded_data = data.decode('utf-8')

    # Step 2: Load the JSON data
    json_data = json.loads(decoded_data)

    # Step 3: Access the 'result_url' field
    result_url = json_data['result_url']

    return result_url """

def get_video_url():
    time.sleep(30)
    url = "https://api.d-id.com/talks"
    headers = {
        "accept": "application/json",
        "Authorization": f"Basic {D_ID_API_KEY}",
    }
    response = requests.get(url, headers=headers)
    data = response.content

    # Step 1: Decode the byte string into a regular string
    decoded_data = data.decode('utf-8')

    # Step 2: Load the JSON data
    json_data = json.loads(decoded_data)

    fields = len(json_data['talks'])
    print(fields)
    # Step 4: Access the 'result_url' field
    print(json_data['talks'][0])
    result_url = json_data['talks'][0]['result_url']
    return result_url

def download_video(video_url):
    options = Options()
    #options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)

    driver.get(video_url)

    wait = WebDriverWait(driver, 10)  
    element = wait.until(EC.presence_of_element_located((By.ID, "example")))
    driver.close()

def get_latest_file():
    directory_path = 'c:/Users/fedor/Downloads/'

    most_recent_file = None
    most_recent_time = 0

    # iterate over the files in the directory using os.scandir
    for entry in os.scandir(directory_path):
        if entry.is_file():
            # get the modification time of the file using entry.stat().st_mtime_ns
            mod_time = entry.stat().st_mtime_ns
            if mod_time > most_recent_time:
                # update the most recent file and its modification time
                most_recent_file = entry.name
                most_recent_time = mod_time
    
    return f"c:/Users/fedor/Downloads/{most_recent_file}"

def PlayVideo(video_path):
    video=cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    while True:
        grabbed, frame=video.read()
        audio_frame, val = player.get_frame()
        if not grabbed:
            print("End of video")
            break
        if cv2.waitKey(40) & 0xFF == ord("q"):
            break
        cv2.imshow("Video", frame)
        if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame
    video.release()
    cv2.destroyAllWindows()

# Главный цикл диалога (3 обмена репликами для примера)
for i in range(3):
    print(f"\n--- Ход {i+1} ---")
    
    # Генерация текста
    reply_text = generate_reply(current_speaker, history)
    history.append({"role": "user", "content": reply_text})

    talk_id = create_avatar_video(current_speaker, reply_text)
    print(f"talk_id: {talk_id}")

    result_url = get_video_url()
    print(f"video url: {result_url}")

    download_video(result_url)

    file = get_latest_file()
    print(f"latest file: {file}")

    PlayVideo(file)
    # Меняем говорящего
    current_speaker, next_speaker = next_speaker, current_speaker
    
    

print("\n--- Дискуссия завершена ---")