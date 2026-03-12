\\backend/app/utils/db_sql.py


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



\\backend/app/utils/db_mongo.py
from pymongo import MongoClient
from flask import current_app

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def init_app(self, app):
        self.client = MongoClient(app.config['MONGO_URI'])
        self.db = self.client['car_rental_mongo']

    @property
    def car_meta(self):
        return self.db['car_metadata']

    @property
    def logs(self):
        return self.db['activity_logs']

    @property
    def cache(self):
        return self.db['search_cache']

mongo = MongoDB()
