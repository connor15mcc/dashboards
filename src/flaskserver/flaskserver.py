from flask import Flask, redirect, url_for, request, render_template
from tracker.tracker import Tracker
from tracker.application import Application
from tracker.event import Event
from typing import List
import tracker.main

# https://testdriven.io/courses/learn-flask/
app = Flask(__name__)

loadedTrackers: List[Tracker] = tracker.main.unpickle_trackers(
    tracker.main.PICKLE_LOCATION
)


@app.route("/")
def homepage():
    return redirect("/trackers/")


@app.route("/trackers/")
def trackers():
    return render_template("trackers.html", trackers=loadedTrackers)


@app.route("/trackers/<tracker_name>/")
def tracker(tracker_name):
    correctTrackers = [x for x in loadedTrackers if x.name == tracker_name]
    if len(correctTrackers) == 0:
        return render_template(
            "error.html", msg="Sorry, no trackers exist with this name."
        )
    elif len(correctTrackers) == 1:
        return render_template("tracker.html", tracker=correctTrackers[0])
    else:
        return render_template(
            "error.html",
            msg="Sorry, multiple trackers exist with that name."
            " Please clean the dataset.",
        )


if __name__ == "__main__":
    app.run(debug=True)
