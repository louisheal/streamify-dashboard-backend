import logging
import os

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

logging.debug(f"Using {DB_USER} to connect to mongodb")

class MongoConfig:
    MONGO_URI = f"mongodb+srv://{DB_USER}:{DB_PASS}@streamify.j2vdk73.mongodb.net/dashboard"
