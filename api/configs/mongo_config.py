import os

from config import config

DB_USER = config.DB_USER
DB_PASS = os.environ.get('DB_PASS')


class MongoConfig:
    MONGO_URI = f"mongodb+srv://{DB_USER}:{DB_PASS}@streamify.j2vdk73.mongodb.net/dashboard"
    MONGO_DBNAME = 'dashboard'
    SESSION_TYPE = 'mongodb'
    SESSION_MONGODB_DB = 'dashboard'
    SESSION_MONGODB_COLLECTION = 'sessions'
