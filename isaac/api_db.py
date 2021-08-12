from flask import json
from isaac.models import Record, Recordbeta
from isaac import app

# ==============================
# API DATATABLES + GLOBAL API(no-cors)
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

@app.route('/api/cat_blue_baby')
def cat_chest():
    data = {'cat_blue_baby': [user.to_dict() for user in Record.query.filter(Record.category == "blue_baby")]}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/api/cat_all_chapter')
def cat_all_chapter():
    data = {'cat_all_chapter': [user.to_dict() for user in Record.query.filter(Record.category == "all_chapter")]}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/api/all_cat')
def data():
    data = {'data': [user.to_dict_all() for user in Record.query]}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# ===============================================
# 
#                     BETA
# 
# ===============================================
@app.route('/beta/api/cat_mother')
def beta_cat_mother():
    data = {'cat_mother': [user.to_dict() for user in Recordbeta.query.filter(Recordbeta.category == 'mother')]}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/beta/api/cat_blue_baby')
def beta_cat_chest():
    data = {'cat_blue_baby': [user.to_dict() for user in Recordbeta.query.filter(Recordbeta.category == "blue_baby")]}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/beta/api/cat_all_chapter')
def beta_cat_all_chapter():
    data = {'cat_all_chapter': [user.to_dict() for user in Recordbeta.query.filter(Recordbeta.category == "all_chapter")]}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
