#!/usr/lib/python3
import time
import requests
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


import os
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False




GENERATED_CLIENT_ID=os.getenv('GENERATED_CLIENT_ID')
SECRET_OAUTH=os.getenv('SECRET_OAUTH')

db = SQLAlchemy(app)


class Recordbeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    streak = db.Column(db.String(128))
    twitch = db.Column(db.String(128))
    category = db.Column(db.String(128))
    channel_id = db.Column(db.String(128))
    status = db.Column(db.String(128))

    def __init__(self,name,twitch,channel_id):
        self.name=name
        self.streak=""
        self.twitch=twitch
        self.category=""
        self.channel_id=channel_id
        self.status = "offline"




#   этот скрипт
#   проверяет онлайн/оффлайн стример 
#   и меняет значение в БД на соответствующее
#   раз в 5 минут
# 


def do_every(period,f,*args):
    def g_tick():
        t = time.time()
        while True:
            t += period
            yield max(t - time.time(),0)
    g = g_tick()
    while True:
        time.sleep(next(g))
        f(*args)

def hello(s):
    all_streamers = Recordbeta.query.all()
    # проверяем, есть ли username в колонке имён
    headers_main = {'Authorization': f'Bearer {SECRET_OAUTH}', "client-id":f"{GENERATED_CLIENT_ID}"}
    for streamer in all_streamers:
        print("check if streamer online: ", streamer.name)
        # проверить онлайн ли стрим
        r = requests.get(url = f"https://api.twitch.tv/helix/streams?user_id={streamer.channel_id}", headers = headers_main)
        print("fine btw")
        try:
            data = r.json()
            try:
                data["data"][0]["game_id"] == "491080" # если на стриме сейчас Isaac.
                #  по сути не важно какая игра - если не вызвало ошибку, значит в json-е есть game_id, а значит стрим онлайн.
                streamer.status = "online"
            except IndexError:
                streamer.status = "offline"
        except:
            print("err occur")
    db.session.commit()
    time.sleep(170)

do_every(1,hello,'statuses are updated')
