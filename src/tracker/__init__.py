from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_breadcrumbs import Breadcrumbs
from flask_scss import Scss

__DEBUG__ = True

# https://testdriven.io/courses/learn-flask/
app = Flask(__name__)
if __DEBUG__:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tracker-test.db"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tracker.db"
db = SQLAlchemy(app)

Breadcrumbs(app=app)

app.debug = __DEBUG__
Scss(app)
