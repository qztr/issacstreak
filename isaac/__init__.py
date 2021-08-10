from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import FileHandler, WARNING, ERROR
from flask_migrate import Migrate
from config import Config

conf = Config()


migrate = Migrate()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = conf.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = conf.SQLALCHEMY_TRACK_MODIFICATIONS
app.secret_key = conf.SECRET_KEY
db = SQLAlchemy(app)
db.init_app(app)
migrate.init_app(app,db)

from isaac import routes, loged_in, api_bot, render_pages, api_db, panels