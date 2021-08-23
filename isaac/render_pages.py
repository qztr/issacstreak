from flask import (flash, redirect, render_template, request, url_for)
from isaac.models import Public_update, Record, Recordbeta
from isaac import app, db
from config import Config


conf = Config()
TWITCH_LOGIN =   conf.TWITCH_LOGIN
CATEGORIES =     conf.CATEGORIES

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
    all_public_updates = Public_update.query.order_by(Public_update.id.desc()).filter(Public_update.is_active != "False").all()
    return render_template('admin_panel.html',all_records=all_records, twitch_login=twitch_login, all_public_updates=all_public_updates)

@app.route('/public_panel', methods = ['GET'])
def public_panel():
    twitch_login = TWITCH_LOGIN
    all_records = Record.query.all()
    return render_template('public_panel.html',all_records=all_records, twitch_login=twitch_login)

@app.route('/terms', methods = ['GET'])
def terms():
    return render_template('terms/terms.html')

@app.route('/policy', methods = ['GET'])
def policy():
    return render_template('terms/policy.html')

@app.route('/bot_policy', methods = ['GET'])
def bot_policy():
    return render_template('terms/bot_policy.html')
