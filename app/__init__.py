from flask import Flask
from flask_pymongo import PyMongo

from .flask_config import FlaskConfig
from .mongo_config import MongoConfig

app = Flask(__name__)

app.config.from_object(FlaskConfig)

app.config.from_object(MongoConfig)

mongo = PyMongo(app)

from . import routes
