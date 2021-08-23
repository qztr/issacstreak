from flask import request
from isaac.models import Record
from isaac import app, db
from config import Config
from isaac.routes import auth_log


conf = Config()

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
    if  request.form['category'] in conf.CATEGORIES:
        streamer = Record.query.filter_by(name =  request.form['channel']).first()
        if streamer is None:
            return("stremer not found")
        else:
            streamer.category = request.form['category']
            db.session.commit()
            auth_log(streamer.name,f"streamer updated category to {streamer.category}")
            return("success")
    else:
        return("err, category not in list")

# по этому роуту бот запрашивает имена всех стримеров, к которым подключится 
@app.route('/api_bot/names', methods = ['GET'])
def names():
    all_names = {}
    q = Record.query.filter(Record.use_bot == True).all()
    for rec in q:
        all_names[rec.name] = rec.name
    return (all_names,200)

