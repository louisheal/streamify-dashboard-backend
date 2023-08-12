import os
import redis
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_session import Session

from .flask_config import FlaskConfig
from .mongo_config import MongoConfig

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

ENV = os.environ.get("FLASK_ENV", "development")

if ENV == "production":
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'session:'
    app.config['SESSION_REDIS'] = redis.StrictRedis(host='redis://red-cjbub0fdb61s73bpajdg', port=6379)
else:
    app.config['SESSION_TYPE'] = 'filesystem'

app.config.from_object(FlaskConfig)
app.config.from_object(MongoConfig)

Session(app)

FRONTEND_URL = os.environ.get('FRONTEND_URL')
CORS(app, supports_credentials=True, origins=[FRONTEND_URL])

mongo = PyMongo(app)

from . import routes
