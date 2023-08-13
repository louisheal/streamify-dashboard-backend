from datetime import timedelta
import os

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_session import Session

from .flask_config import FlaskConfig
from .mongo_config import MongoConfig

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

app.config.from_object(FlaskConfig)
app.config.from_object(MongoConfig)

mongo = PyMongo(app)

app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config["SESSION_TYPE"] = 'mongodb'
app.config["SESSION_MONGODB"] = mongo.cx
app.config["SESSION_MONGODB_DB"] = 'dashboard'
app.config["SESSION_MONGODB_COLLECTION"] = 'sessions'

Session(app)

FRONTEND_URL = os.environ.get('FRONTEND_URL')
CORS(app, supports_credentials=True, origins=[FRONTEND_URL])

from . import routes
