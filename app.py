# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask
from flask import request
from flask.wrappers import Response
import re
import os
import pafy
import time


app = Flask(__name__)

def write_json(data, filename='response.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def send_message(chat_id, text='bla-bla-bla'):
    url = f'https://api.telegram.org/bot{os.getenv("token_bot")}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    r = requests.post(url, json=payload)
    return r


def parse_message(message):

    chat_id = message['message']['chat']['id'] if message.get('message') else message['edited_message']['chat']['id']
    txt = message['message']['text'] if message.get('message') else message['edited_message']['text']

    print(chat_id, txt)

    pattern = r'''(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*?[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'''

    videoid_youtube = re.findall(pattern, txt)

    if not videoid_youtube:
        if "/start" in txt:
            videoid_youtube = str(txt)

    return chat_id, videoid_youtube

def process_url(youtube, chat_id):

    video = pafy.new(youtube)
    print('title:', video.title)

    if video.title is not None:
        audiom4a = video.getbestaudio(preftype="m4a")
        audiom4a.download(quiet=True)
        url = f'https://api.telegram.org/bot{os.getenv("token_bot")}/sendAudio?chat_id={chat_id}&title={audiom4a.title}'

        r = requests.post(url, files={'audio': open(r'./'+video.title+'.m4a', 'rb')})
        time.sleep(20)
        r.close()
        os.remove(r'./'+video.title+'.m4a')

    return Response('ok', status=200)



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, videoid_youtube = parse_message(msg)

        print('videoid:', videoid_youtube)

        if videoid_youtube != type(int):        
            if "/start" in videoid_youtube:
                    send_message(chat_id, """Welcome to MP3Youtube Bot, the bot can be used to download songs from your favorite YouTube videos, so enter the video URL, for example (www.youtube.com/watch?v=F1B9Fk_SgI0) and the bot will respond with the audio file.""")

            elif videoid_youtube:
                process_url(videoid_youtube[0], chat_id)
                write_json(msg, 'telegram_request.json')

            else:
                send_message(chat_id, "Please, send a valid video url.")
        else:
            send_message(chat_id, "Please, send a valid video url.")

        return Response('ok', status=200)
    else:
        return '<h2><title>It works</title>It works</h2>'
