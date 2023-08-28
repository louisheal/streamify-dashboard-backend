import os

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_session import Session

from api.configs.flask_config import FlaskConfig
from api.configs.mongo_config import MongoConfig
from config import config

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

app.config.from_object(FlaskConfig)
app.config.from_object(MongoConfig)

mongo = PyMongo(app)
app.config['SESSION_MONGODB'] = mongo.cx

Session(app)

CORS(app, supports_credentials=True, origins=[config.FRONTEND_URL])

from api import routes
