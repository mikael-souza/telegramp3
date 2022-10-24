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
from random import randint
import threading


app = Flask(__name__)

def write_json(data, filename='response.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def send_message_start(chat_id, text='bla-bla-bla'):
    # url = f'https://api.telegram.org/bot{os.getenv("token_bot")}/sendMessage'
    url = f'https://api.telegram.org/bot520464277:AAEeUwJWImdIOUkezNiVjjLzD_xtn6xMFXk/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    r = requests.post(url, json=payload)

    print(r.text)
    return r

def send_message_reply(chat_id, msg_id, text='bla-bla-bla'):
    # url = f'https://api.telegram.org/bot{os.getenv("token_bot")}/sendMessage'
    url = f'https://api.telegram.org/bot520464277:AAEeUwJWImdIOUkezNiVjjLzD_xtn6xMFXk/sendMessage'
    payload = {'chat_id': chat_id, 'reply_to_message_id': msg_id, 'text': text}

    r = requests.post(url, json=payload)

    print(r.text)
    return r


def parse_message(message):

    msg_id = message['message']['message_id'] if message.get('message') else message['edited_message']['message_id']
    chat_id = message['message']['chat']['id'] if message.get('message') else message['edited_message']['chat']['id']
    txt = message['message']['text'] if message.get('message') else message['edited_message']['text']

    print(chat_id, txt, msg_id)

    pattern = r'''(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*?[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'''

    videoid_youtube = re.findall(pattern, txt)

    if not videoid_youtube:
        if "/start" in txt:
            videoid_youtube = str(txt)

    return chat_id, msg_id, videoid_youtube

def process_url(youtube, msg_id, chat_id):

    file_name = randint(123456789,987654321)
    video = pafy.new(youtube)
    print('title:', video.title)

    if video.title is not None:
        audiom4a = video.getbestaudio(preftype="m4a")
        audiom4a.download(quiet=True, filepath=rf"./{file_name}.m4a", meta=True)
        # url = f'https://api.telegram.org/bot{os.getenv("token_bot")}/sendAudio?&reply_to_message_id={msg_id}&title={audiom4a.title}'
        url = f'https://api.telegram.org/bot520464277:AAEeUwJWImdIOUkezNiVjjLzD_xtn6xMFXk/sendAudio?&chat_id={chat_id}&reply_to_message_id={msg_id}&title={audiom4a.title}'

        r = requests.post(url, files={'audio': open(rf'./{file_name}.m4a', 'rb')})
        r.close()
        #time.sleep(30)
    os.remove(rf'./{file_name}.m4a')

    return Response('ok', status=200)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, msg_id, videoid_youtube = parse_message(msg)

        print('videoid:', videoid_youtube)

        if videoid_youtube != type(int):        
            if "/start" in videoid_youtube:
                    send_message_start(chat_id, """Welcome to MP3Youtube Bot, the bot can be used to download songs from your favorite YouTube videos, so enter the video URL, for example (www.youtube.com/watch?v=F1B9Fk_SgI0) and the bot will respond with the audio file.""")

            elif videoid_youtube:
                send_message_start(chat_id, "Please wait, we are converting your video to audio!")
                try:
                    threading.Thread(target=process_url, args=(videoid_youtube[0], msg_id, chat_id,)).start()
                    time.sleep(2)
                except Exception as e:
                    print(e)
                # process_url(videoid_youtube[0], msg_id, chat_id)
                write_json(msg, 'telegram_request.json')

            else:
                send_message_reply(chat_id, msg_id, "Please, send a valid video url.")
        else:
            send_message_reply(chat_id, msg_id, "Please, send a valid video url.")

        return Response('ok', status=200)
    else:
        return '<h2><title>It works</title>It works</h2>'
