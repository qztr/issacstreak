import requests
import re
from isaac.models import RecordBETA
from threading import Thread
from isaac import db


GENERATED_CLIENT_ID=os.getenv('GENERATED_CLIENT_ID')
SECRET_OAUTH=os.getenv('SECRET_OAUTH')

# pass only current streak value
def update(current_streak,id):
    # нас случай, если переменная не ИНТ
    try:
        print(int(current_streak))
    except:
        pass
    streamer = Record.query.filter(Record.id == id).first()
    if streamer is not None:
        streamer.current = current_streak
        if int(current_streak) > streamer.best: # меняем так же PB на новое значение
            streamer.best = current_streak
        db.session.commit()
    else:
        pass

def reg1(title,id):
    title1 = re.compile("\d+\s*-\s*\d+")
    streak1 = title1.findall(title)[0]
    take_number = re.compile("\d+")
    number2 = take_number.findall(streak1)[0]
    update(number2,id)

def reg2(title,id):
    title2 = re.compile("[[(]\s*\d+\s*[])]")
    streak2 = title2.findall(title)
    take_number = re.compile("\d+")
    number2 = take_number.findall(streak2)[0]
    update(number2,id)

def reg3(title,id):
    title3 = re.compile("[cC].*:\s*\d+")
    take_number = re.compile("\d+")
    streak3 = title3.findall(title)
    number3_curr = take_number.findall(streak3)[0] # current
    number3_best = take_number.findall(streak3)[0] # PB
    update(number3_curr,id)


def main_th(channel_id,id):
    headers_main = {'Authorization': f'Bearer {SECRET_OAUTH}', "client-id":f"{GENERATED_CLIENT_ID}"}

    r = requests.get(url = f"https://api.twitch.tv/helix/streams?user_id={channel_id}", headers = headers_main)
    data = r.json()
    try:
        title = (data['data'][0]['title']) # если тайтл есть - не выдаст ошибку, можно запускать потоки с регулярками
        reg1(title,id)
        reg2(title,id)
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


threads_main()

