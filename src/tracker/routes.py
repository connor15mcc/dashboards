from flask import redirect, url_for, render_template
from flask_breadcrumbs import register_breadcrumb
from tracker import app
from tracker.models import Tracker, Application, Event

exampleTrackers = [
    Tracker(
        name_id="fall_2021",
        name="Fall 2021",
        desc="Applications for summer 2022 internships",
        applications=[],
    ),
    Tracker(
        name_id="fall_2022",
        name="Fall 2022",
        desc="Applications for full-time employment",
        applications=[
            Application(
                application_id=0,
                company_name="Connor's Store",
                position_name="SWE",
                event_history=[
                    Event(event_id=1, desc="applied", from_me=True),
                    Event(event_id=2, desc="rejected", from_me=False),
                ],
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
@register_breadcrumb(app, ".", "Home")
def allTrackers():
    return render_template("trackers.html", title="Trackers", trackers=exampleTrackers)


@app.route("/trackers/<tracker_name>/")
@register_breadcrumb(app, ".trackername", "Tracker")
def oneTracker(tracker_name):
    correctTrackers = [x for x in exampleTrackers if x.name_id == tracker_name]
    if len(correctTrackers) == 0:
        return render_template(
            "error.html", msg="Sorry, no trackers exist with this name."
        )
    elif len(correctTrackers) == 1:
        return render_template(
            "tracker.html",
            title=[x for x in exampleTrackers if x.name_id == tracker_name][0].name,
            tracker=correctTrackers[0],
        )
    else:
        return render_template(
            "error.html",
            msg="Sorry, multiple trackers exist with that name."
            " Please clean the dataset.",
        )


@app.route("/trackers/<tracker_name>/<app_id>")
@register_breadcrumb(app, ".trackername.application", "Application")
def oneApplication(tracker_name, app_id):
    correctTracker = [x for x in exampleTrackers if x.name_id == tracker_name][0]
    # TODO ^ verify this is correct length (and below)
    correctApplication = [
        x for x in correctTracker.applications if x.application_id == int(app_id)
    ][0]
    return render_template(
        "application.html",
        title=correctApplication.company_name,
        application=correctApplication,
    )
