import requests
import json
import os

API_URL = f'https://api.telegram.org/bot{os.getenv("BOT_TOKEN")}'
youtube_regex = "https:\/+[a-zA-Z]+\/[a-zA-Z0-9\_-]+|www\.youtube\.com\/[a-zA-Z0-9\_-]+|youtube\/[a-zA-Z0-9\_-]+|youtu.be\/[a-zA-Z0-9\_-]+|^https:\/\/youtu.be+\/+[a-zA-Z0-9\_-]+|youtube\.com\/watch\?v=+[a-zA-Z0-9\_-]+|^https:\/\/www\.youtube\.com\/watch\?v=+[a-zA-Z0-9\_-]+"

def processMessage(message):
    message_id = message['message_id']
    chat_id = message['chat']['id']
    if message['text']:
        text = message['text']
        
        def sendMessage(message):
            uri = f"{API_URL}/sendMessage?"
            headers = {'content-type': 'application/json'}
            payload = {
                    "chat_id": chat_id,
                    "text": text}
            response = requests.post(uri, data=json.dumps(payload), headers=headers).json()
        
        
        
        if text == "/start":
            sendMessage(f"Olá, {message['from']['first_name']} \nEu sou um Bot que te ajudará com o download de músicas do YouTube, cole o link do vídeo abaixo!")