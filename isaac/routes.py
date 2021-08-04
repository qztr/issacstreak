from flask import (flash, redirect, render_template, request, url_for, session,send_from_directory, jsonify, json)
import os
import csv
import flask
from isaac.models import Record, Secrets
from isaac import app, db
import requests
import time
from config import Config
import cryptocode


conf = Config()
SCOPES =         conf.SCOPES
CLIENT_ID =      conf.CLIENT_ID
REDIRECT_URI =   conf.REDIRECT_URI
SECRET_OAUTH =   conf.SECRET_OAUTH
TWITCH_LOGIN =   conf.TWITCH_LOGIN
KEY_FOR_API = conf.KEY_FOR_API
CATEGORIES =     conf.CATEGORIES
CLIENT_SECRET =  conf.CLIENT_SECRET
GENERATED_CLIENT_ID = conf.GENERATED_CLIENT_ID


# =====================================
# на этот роут редиректит успешная авторизация twitch
# =====================================
@app.route('/loged_in')
def login():
    recived_code = request.args.get("code") # после подтвержденной авторизации и редиректа со стр твича, получаем как агрумент code
    if recived_code is None:
        print("no code get")
        return redirect(url_for("single"))

    url = f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={recived_code}&grant_type=authorization_code&redirect_uri={REDIRECT_URI}"
    r = requests.post(url)
    data = r.json()

    # /userifno 
    # в ответе получаем preferred_username
    try:
        headers_userifno = {'Authorization': f'Bearer {data["access_token"]}', "client-id":f"{CLIENT_ID}"}
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
    headers_main = {'Authorization': f'Bearer {SECRET_OAUTH}', "client-id":f"{GENERATED_CLIENT_ID}"}

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
            with open('/isaac/isaac/static/csv/user_token.csv','a', newline='') as csv_file: # заносим в csv значения
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

# ==============================
# API BOT 
# ==============================

@app.route('/api_bot/streak', methods = ['POST'])
def api_streak():
    if int(request.form['streak']) < 10000:
        streamer = Record.query.filter_by(name = request.form['channel']).first()
        if streamer is None:
            return("stremer not found")
        else:
            if int(request.form['streak']) > int(streamer.best):
                streamer.best = request.form['streak']
                auth_log(streamer.name,f"streamer best updated streak to {streamer.current}")

            streamer.current = int(request.form['streak'])
            db.session.commit()
            auth_log(streamer.name,f"streamer current updated streak to {streamer.current}")
            return ("success")
    return("smthng wrong")


@app.route('/api_bot/best', methods = ['POST'])
def api_best():
    if int(request.form['best']) < 10000:
        streamer = Record.query.filter_by(name = request.form['channel']).first()
        if streamer is None:
            return("stremer not found")
        else:
            streamer.best = int(request.form['best'])
            db.session.commit()
            auth_log(streamer.name,f"streamer best updated streak to {streamer.best}")
            return ("success")
    return("smthng wrong")
    
@app.route('/api_bot/category', methods = ['POST'])
def api_category():
    if  request.form['category'] in CATEGORIES:
        streamer = Record.query.filter_by(name =  request.form['channel']).first()
        if streamer is None:
            return("stremer not found")
        else:
            streamer.category = request.form['category']
            db.session.commit()
            auth_log(streamer.name,f"streamer updated category to {streamer.category}")
            return("success")
    else:
        return("err, category not in list") # коды на угад 501 - 503 

# по этому роуту бот запрашивает имена всех стримеров, к которым подключится 
@app.route('/api_bot/names', methods = ['GET'])
def names():
    all_names = {}
    q = Record.query.all()
    for rec in q:
        all_names[rec.name] = rec.name
    return (all_names,200)



# ==============================
# API DATATABLES  
# ==============================
# этот роут использует таблица DataTables на главной странице
@app.route('/api/cat_mother')
def cat_mother():
    data = {'cat_mother': [user.to_dict() for user in Record.query.filter(Record.category == 'mother')]}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/api/cat_chest')
def cat_chest():
    data = {'cat_chest': [user.to_dict() for user in Record.query.filter(Record.category == "chest")]}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/api/cat_all_bosses')
def cat_all_bosses():
    data = {'cat_all_bosses': [user.to_dict() for user in Record.query.filter(Record.category == "all_bosses")]}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/api/all_cat')
def data():
    data = {'data': [user.to_dict() for user in Record.query]}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response



# ==============================
# Render pages 
# ==============================
@app.route('/', methods = ['GET'])
def single():
    twitch_login = TWITCH_LOGIN
    all_records = Record.query.all()
    return render_template('single_dt.html',all_records=all_records, twitch_login=twitch_login)

@app.route('/bot', methods = ['GET'])
def bot_page():
    twitch_login = TWITCH_LOGIN
    return render_template('bot_page.html', twitch_login = twitch_login)

@app.route('/mother', methods = ['GET'])
@app.route('/eden', methods = ['GET'])
@app.route('/chest', methods = ['GET'])
def go_main_page():
    return redirect(url_for("single"))

@app.route('/admin_panel', methods = ['GET'])
def admin_panel():
    twitch_login = TWITCH_LOGIN
    all_records = Record.query.all()
    return render_template('admin_panel.html',all_records=all_records, twitch_login=twitch_login)


@app.route('/admin_edit', methods = ['POST','GET'])
def admin_edit():
    q = Record.query.all()
    if request.method == 'POST':
        req = request.form
        access_admin = Secrets.query.filter(Secrets.key == req.get("secret_password")).first()
        if access_admin is not None:
            for record in q:
                curr = req.get(f"{record.name}_current")
                best = req.get(f"{record.name}_best")
                cat =  req.get(f"{record.name}_category")

                if int(curr) < 10000:
                    record.current = curr
                if int(best) < 10000:
                    record.best = best
                if cat in CATEGORIES:
                    record.category = cat
            db.session.commit()
            flash("success")
        else:
            flash("access denied")

    return (redirect(url_for("admin_panel")))



# =====================================
# (\/)_(q__p)_(\/)
# =====================================

# логгировать события
def auth_log(username,msg):
    with open('/isaac/isaac/static/csv/auth_log.csv','a', newline='') as csv_file:
        write_csv = csv.writer(csv_file,  delimiter=',')
        write_csv.writerow([time.ctime(), request.remote_addr, username, msg])

# добавить стримера в бд
def add_to_table(username, channel_id):
    twitch = f"https://www.twitch.tv/{username.lower()}"
    new_streamer = Record(username,twitch, channel_id)
    db.session.add(new_streamer)
    db.session.commit()
    print("стример добавлен")

# скачать логи
@app.route('/log/<token>', methods = [ 'GET' ])
def log(token):
    if token == os.environ.get('token'):
        filename = os.path.join('{0}'.format(conf.PATH_TO_LOGFILE), '%s.log' % 'logfile')
        return flask.send_file(filename, as_attachment=True) 
    else:
        return redirect(url_for("mother"))

# файл индексации гугла, чтобы показывать сайт в поиске(yandex пока не ищет! в РФ половина аудитории)
@app.route('/googleauth/', methods = ['GET'])
def googleauth():
    return render_template('googlec173659fa84364dd.html')

@app.route('/sitemap.xml', methods = ['GET'])
def sitemap():
    return send_from_directory(app.static_folder, request.path[1:])



if __name__ == "__main__":
    app.run()
