from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_breadcrumbs import Breadcrumbs
from flask_scss import Scss
import os
from dotenv import load_dotenv

__DEBUG__ = True

# https://testdriven.io/courses/learn-flask/
app = Flask(__name__)

load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "for dev")
if __DEBUG__:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tracker-test.db"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

Breadcrumbs(app=app)

app.debug = __DEBUG__
Scss(app)
