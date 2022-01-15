from dotenv import load_dotenv
import os


load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///dashboards.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigTest:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///dashboards.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
