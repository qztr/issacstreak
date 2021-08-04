from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import FileHandler, WARNING, ERROR
from flask_migrate import Migrate

migrate = Migrate()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('secret_key')
logging.basicConfig(filename='logfile02.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
db = SQLAlchemy(app)
db.init_app(app)
migrate.init_app(app,db)