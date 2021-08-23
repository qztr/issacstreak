import requests
import re
from isaac.models import Record
from threading import Thread
from isaac import db
import time
import csv
import os
from dotenv import load_dotenv
import threading
import sys



load_dotenv()

PATH_TO_CSV = "/home/qztr-1/coding/isaac-chaos/isaac-streak-0.3/flask"
GENERATED_CLIENT_ID= os.getenv("GENERATED_CLIENT_ID")
SECRET_OAUTH = os.getenv('SECRET_OAUTH')


GENERATED_CLIENT_ID=os.getenv('GENERATED_CLIENT_ID')
SECRET_OAUTH=os.getenv('SECRET_OAUTH')

# pass only current streak value
def update(current_streak,id):
    # нас случай, если переменная не ИНТ
    # print(current_streak,id)
    try:
        print(int(current_streak))
    except:
        pass
    streamer = Record.query.filter(Record.id == id).first()
    if streamer is not None:
        if not {streamer.current} == {current_streak}:
            auto_updates_log(f'{streamer.name}(current) : {streamer.current} -> {current_streak}')
            streamer.current = current_streak
            db.session.commit()
            if int(current_streak) > int(streamer.best): # меняем так же PB на новое значение
                streamer.best = current_streak
                db.session.commit()

    else:
        print("streamer is none but it will be not printed anywhere")
        pass

# (12-0) / [12-0]
def reg1(title,id):
    title1 = re.compile("\d+\s*-\s*\d+")
    streak1 = title1.findall(title)[0]
    take_number = re.compile("\d+")
    number2 = take_number.findall(streak1)[0]
    update(number2,id)

# [12]
def reg2(title,id):
    title2 = re.compile("[[(]\s*\d+\s*[])]")
    streak2 = title2.findall(title)[0]
    take_number = re.compile("\d+")
    number2 = take_number.findall(streak2)[0]

    update(number2,id)

# C:12
def reg3(title,id):
    title3 = re.compile("\d*[cC]\s*:\s*\d+")
    take_number = re.compile("\d+")
    streak3 = title3.findall(title)[0]
    number3_curr = take_number.findall(streak3)[0] # current
    update(number3_curr,id)
    # строка ниже крашит функцию, если не было "PB:888" в title (888 - случайное число)
    # number3_best = take_number.findall(streak3)[1] # PB


def main_th(channel_id,id):
    headers_main = {'Authorization': f'Bearer {SECRET_OAUTH}', "client-id":f"{GENERATED_CLIENT_ID}"}

    r = requests.get(url = f"https://api.twitch.tv/helix/streams?user_id={channel_id}", headers = headers_main)
    data = r.json()

    try: # если тайтл есть - не выдаст ошибку, можно запускать потоки с регулярками
        title = (data['data'][0]['title']) 
    except:
        pass
    try:
        reg1(title,id)
    except:
        pass
    try:
        reg2(title,id)
    except:
        pass
    try:
        reg3(title,id)
    except:
        pass
    


def threads_main():
    records = Record.query.all()
    threads = [Thread(target=main_th, args=(str(record.channel_id),str(record.id))) for record in records]
    # start the threads
    for thread in threads:
        thread.start()
    # wait for the threads to complete
    for thread in threads:
        thread.join()
    # time.sleep(300)
    
def auto_updates_log(msg):
    with open(f'{PATH_TO_CSV}/auto_updates.csv','a', newline='') as csv_file:
        write_csv = csv.writer(csv_file,  delimiter=',')
        write_csv.writerow([time.ctime(),msg])
        csv_file.close()

# def do_every(period,f,*args):
#     def g_tick():
#         t = time.time()
#         while True:
#             t += period
#             yield max(t - time.time(),0)
#     g = g_tick()
#     while True:
#         time.sleep(next(g))
#         f()

def restart():
    threads_main()
    print("restart now")
    os.execv(sys.executable, ['python'] + sys.argv)
            
# перезапуск бота, чтобы он мог раз в 5 мин подключаться к каналам, которые стали ОНЛАЙН
def reload():
    threading.Timer(30, restart).start() # время, через которое запускать функцию - в секундах.


reload()

# do_every(1,threads_main,'updated')
