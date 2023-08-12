import os

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

from .flask_config import FlaskConfig
from .mongo_config import MongoConfig

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(FlaskConfig)
app.config.from_object(MongoConfig)

FRONTEND_URL = os.environ.get('FRONTEND_URL')
CORS(app, supports_credentials=True, origins=[FRONTEND_URL])

mongo = PyMongo(app)

from . import routes
