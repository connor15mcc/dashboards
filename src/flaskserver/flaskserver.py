from flask import Flask, redirect, url_for, render_template
from tracker.tracker import Tracker
from typing import List
import tracker.main
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# https://testdriven.io/courses/learn-flask/
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


class Tracker(db.Model):
    name_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    applications = db.relationship("Application", backref="tracker", lazy=True)

    def __repr__(self):
        return f"Tracker('{self.name_id}', '{self.desc}')"


class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    position_name = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    link = db.Column(db.String)
    status = db.Column(db.String, nullable=False)
    of_tracker = db.Column(db.String, db.ForeignKey("tracker.name_id"), nullable=False)
    event_history = db.relationship("Event", backref="application", lazy=True)

    def __repr__(self):
        return f"Application('{self.application_id}', '{self.company_name}', '{self.position_name}'"


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String, nullable=False)
    from_me = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    of_application = db.Column(
        db.Integer, db.ForeignKey("application.application_id"), nullable=False
    )

    def __repr__(self):
        return f"Event('{self.event_id}', '{self.desc}', '{self.date}')"


@app.route("/")
def homepage():
    return redirect(url_for("trackers"))


@app.route("/trackers/")
def trackers():
    return render_template("trackers.html", title="Trackers", trackers=loadedTrackers)


@app.route("/trackers/<tracker_name>/")
def tracker(tracker_name):
    correctTrackers = [x for x in loadedTrackers if x.name == tracker_name]
    if len(correctTrackers) == 0:
        return render_template(
            "error.html", msg="Sorry, no trackers exist with this name."
        )
    elif len(correctTrackers) == 1:
        return render_template(
            "tracker.html", title=tracker_name, tracker=correctTrackers[0]
        )
    else:
        return render_template(
            "error.html",
            msg="Sorry, multiple trackers exist with that name."
            " Please clean the dataset.",
        )


if __name__ == "__main__":
    app.run(debug=True)
