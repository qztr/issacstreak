from flask import (flash, redirect, render_template, request, url_for)
import csv
from isaac.models import Record
from isaac import app
import requests
import time
from config import Config
from isaac.routes import add_to_table,auth_log


conf = Config()

# =====================================
# на этот роут редиректит успешная авторизация twitch
# =====================================
@app.route('/loged_in')
def login():
    recived_code = request.args.get("code") # после подтвержденной авторизации и редиректа со стр твича, получаем как агрумент code
    if recived_code is None:
        print("no code get")
        return redirect(url_for("single"))

    url = f"https://id.twitch.tv/oauth2/token?conf.CLIENT_ID={conf.CLIENT_ID}&conf.CLIENT_SECRET={conf.CLIENT_SECRET}&code={recived_code}&grant_type=authorization_code&conf.REDIRECT_URI={conf.REDIRECT_URI}"
    r = requests.post(url)
    data = r.json()

    # /userifno 
    # в ответе получаем preferred_username
    try:
        headers_userifno = {'Authorization': f'Bearer {data["access_token"]}', "client-id":f"{conf.CLIENT_ID}"}
    except KeyError:
        return redirect(url_for("single"))
        
    r = requests.get(url = "https://id.twitch.tv/oauth2/userinfo", headers = headers_userifno)
    data = r.json()
    username = data['preferred_username'].lower()
    # проверяем, есть ли username в DB
    streamer = Record.query.filter_by(name = username).first()
    if streamer is not None:
        flash("Seems you aleady in leaderbord!")
        auth_log(username,"streamer already in list")
        return redirect(url_for("bot_page"))
    
    # получаем ИД по preferred_username
    headers_main = {'Authorization': f'Bearer {conf.SECRET_OAUTH}', "client-id":f"{conf.GENERATED_CLIENT_ID}"}

    r = requests.get(url = f"https://api.twitch.tv/helix/users?login={username}", headers = headers_main)
    data = r.json()
    print(data)
    to_id = data['data'][0]['id']

    # проверить стримит ли айзека сейчас
    r = requests.get(url = f"https://api.twitch.tv/helix/streams?user_id={to_id}", headers = headers_main)
    data = r.json()

    try:
        if data["data"][0]["game_id"] == "491080": # если на стриме сейчас Isaac( game_id игры The Binding of Isaac: Repentance на твиче = 491080)
            # бот подписывается на канал по ИД
            raw_data = {"to_id": f"{to_id}","from_id": "710193836"} # from_id - в этом случае это isaac_streak ID : 710193836
            r = requests.post(url = "https://api.twitch.tv/helix/users/follows", headers = headers_main, data=raw_data) # этот реквест ничего не возвращает
            # добавлять в таблицу мета(нет) данные
            with open(f'{conf.PATH_TO_CSV}/user_token.csv','a', newline='') as csv_file: # заносим в csv значения
                write_csv = csv.writer(csv_file,  delimiter=',')
                write_csv.writerow([time.ctime(),request.remote_addr, recived_code, username, to_id])
            csv_file.close()
            add_to_table(username,to_id)
            flash("You have been added to leaderbord! Bot will connect to your chat during next 5 mins")
            auth_log(username,"streamer added")
        else:
            flash("Seems you don`t stream Isaac at the moment. Try again when start Isaac stream")
            auth_log(username,"stream diff game")
    except IndexError:
            flash("Seems your stream is offline at the moment. Try again when start Isaac stream")
            auth_log(username,"stream is offline")


    # # info by login(username)
    # r = requests.get(url = f"https://api.twitch.tv/helix/users?login=daxak", headers = headers_main)
    # data = r.json()
    # print(data)

    return render_template('bot_page.html')