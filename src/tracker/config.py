import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///tracker.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigTest:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///tracker-test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
