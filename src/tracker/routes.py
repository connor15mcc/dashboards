from flask import redirect, url_for, render_template
from tracker import app
from tracker.models import Tracker, Application

exampleTrackers = [
    Tracker(
        name_id="fall_2021",
        name="Fall 2021",
        desc="Applications for Summer 2022",
        applications=[],
    ),
    Tracker(
        name_id="fall_2022",
        name="Fall 2022",
        desc="Applications for full time",
        applications=[
            Application(
                application_id=0, company_name="Connor's Store", position_name="SWE"
            ),
            Application(
                application_id=1, company_name="Connor's Donuts", position_name="SDE"
            ),
        ],
    ),
]


@app.route("/")
def root():
    return redirect(url_for("allTrackers"))


@app.route("/trackers/")
def allTrackers():
    return render_template("trackers.html", title="Trackers", trackers=exampleTrackers)


@app.route("/trackers/<tracker_name>/")
def oneTracker(tracker_name):
    correctTrackers = [x for x in exampleTrackers if x.name_id == tracker_name]
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
