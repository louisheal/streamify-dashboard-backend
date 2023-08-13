import os

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

class MongoConfig:
    MONGO_URI = f"mongodb+srv://{DB_USER}:{DB_PASS}@streamify.j2vdk73.mongodb.net/dashboard"
    MONGO_DBNAME = 'dashboard'
