import os, sys
import logging
from flask import Flask
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy

db_user = os.getenv("POSTGRES_USER")
db_passwd = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_database = os.getenv("POSTGRES_DB")

class Factory:
    def __init__(self, **kwargs):
        self.app = self.create_app(**kwargs)
        self.db = self.get_db()


    def get_db(self, app=None):
        if not hasattr(self, "db") or self.db is None:
            self.db = SQLAlchemy()

        if app is not None:
            self.db.init_app(app)

        return self.db


    def create_app(self, **kwargs):
        if hasattr(self, 'app') and self.app is not None:
            return self.app

        self.app = Flask(__name__, **kwargs)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_database}"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
        self.app.config["APP_SECRET_KEY"] = os.getenv("APP_SECRET_KEY")

        self.db = self.get_db(self.app)

        if "create_db" in kwargs and kwargs["create_db"]:
            with self.app.test_request_context():
                self.db.create_all()

        return self.app

    def get_logger(self):
        for logger in (
            self.create_app().logger,
            logging.getLogger("sqlalchemy")
        ):
            logger.addHandler(default_handler)


        return self.app.logger

