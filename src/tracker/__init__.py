from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_breadcrumbs import Breadcrumbs
from flask_scss import Scss

# https://testdriven.io/courses/learn-flask/
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

Breadcrumbs(app=app)

app.debug = True
Scss(app)
