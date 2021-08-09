from flask import (render_template, request,send_from_directory)
import csv
from isaac.models import Record
from isaac import app, db
import time
from config import Config

conf = Config()

# =====================================
# (\/)_(^__^)_(\/)
# =====================================

# логгировать события
def auth_log(username,msg):
    with open(f'{conf.AUTH_LOG}','a', newline='') as csv_file:
        write_csv = csv.writer(csv_file,  delimiter=',')
        write_csv.writerow([time.ctime(), request.remote_addr, username, msg])

# добавить стримера в бд
def add_to_table(username, channel_id):
    twitch = f"https://www.twitch.tv/{username.lower()}"
    new_streamer = Record(username,twitch, channel_id)
    db.session.add(new_streamer)
    db.session.commit()
    print("стример добавлен")

# файл индексации гугла, чтобы показывать сайт в поиске(yandex пока не ищет! в РФ половина аудитории)
@app.route('/googleauth/', methods = ['GET'])
def googleauth():
    return render_template('googlec173659fa84364dd.html')

# файл индексации гугла, чтобы показывать сайт в поиске(yandex пока не ищет! в РФ половина аудитории)
@app.route('/yandex_471249ab8780be9f.html', methods = ['GET'])
def yaauth():
    return render_template('yandex_471249ab8780be9f.html')

# now working
@app.route('/sitemap.xml', methods = ['GET'])
def sitemap():
    return send_from_directory(app.static_folder, request.path[1:])
