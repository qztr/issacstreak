from flask import json
from isaac.models import Record
from isaac import app

# ==============================
# API DATATABLES + GLOBAL API(no-cors)
# ==============================
# этот роут использует таблица DataTables на главной странице
@app.route("/api/cat_mother")
def cat_mother():
    data = {
        "cat_mother": [
            user.to_dict() for user in Record.query.filter(Record.category == "mother")
        ]
    }
    response = app.response_class(
        response=json.dumps(data), mimetype="application/json"
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/api/cat_blue_baby")
def cat_chest():
    data = {
        "cat_blue_baby": [
            user.to_dict()
            for user in Record.query.filter(Record.category == "blue_baby")
        ]
    }
    response = app.response_class(
        response=json.dumps(data), mimetype="application/json"
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/api/cat_all_chapter")
def cat_all_chapter():
    data = {
        "cat_all_chapter": [
            user.to_dict()
            for user in Record.query.filter(Record.category == "all_chapter")
        ]
    }
    response = app.response_class(
        response=json.dumps(data), mimetype="application/json"
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/api/all_cat")
def data():
    data = {"data": [user.to_dict_all() for user in Record.query]}
    response = app.response_class(
        response=json.dumps(data), mimetype="application/json"
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/api/lost")
def cat_lost():
    """Lost category"""
    data = {
        "cat_lost": [
            user.to_dict()
            for user in Record.query.filter(Record.category == "cat_lost")
        ]
    }
    response = app.response_class(
        response=json.dumps(data), mimetype="application/json"
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/api/t_lost")
def cat_t_lost():
    """Lost category"""
    data = {
        "cat_t_lost": [
            user.to_dict()
            for user in Record.query.filter(Record.category == "cat_t_lost")
        ]
    }
    response = app.response_class(
        response=json.dumps(data), mimetype="application/json"
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
