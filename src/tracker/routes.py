from flask import request, redirect, url_for, render_template
from flask_breadcrumbs import register_breadcrumb
from tracker import app
from tracker.models import Tracker, Application


@app.route("/")
def root():
    return redirect(url_for("allTrackers"))


@app.route("/trackers/")
@register_breadcrumb(app, ".", "Home")
def allTrackers():
    return render_template(
        "trackers.html", title="Trackers", trackers=Tracker.query.all()
    )


@app.route("/trackers/<tracker_name>/")
@register_breadcrumb(app, ".tracker", "Tracker")
def oneTracker(tracker_name):
    correctTracker = Tracker.query.filter_by(name_id=tracker_name).all()
    if len(correctTracker) == 0:
        return render_template(
            "error.html", msg="Sorry, no trackers exist with this name."
        )
    elif len(correctTracker) == 1:
        return render_template(
            "tracker.html",
            title=correctTracker[0].name,
            tracker=correctTracker[0],
        )
    else:
        return render_template(
            "error.html",
            msg="Sorry, multiple trackers exist with that name."
            " Please clean the dataset.",
        )


def breadcrumb_for_oneApplication(*args, **kwargs):
    app_id = request.view_args["app_id"]
    app = Application.query.get(app_id)
    print(f"{app.application_id=}")
    return [{"text": app.company_name, "url": app.application_id}]


@app.route("/trackers/<tracker_name>/<app_id>")
@register_breadcrumb(
    app,
    ".tracker.application",
    "Application",
    dynamic_list_constructor=breadcrumb_for_oneApplication,
)
def oneApplication(tracker_name, app_id):
    correctTracker = Tracker.query.filter_by(name_id=tracker_name).all()
    if len(correctTracker) != 1:
        return render_template(
            "error.html",
            msg="Sorry, either zero or multiple trackers exist with that name."
            " Please clean the dataset.",
        )
    correctTracker = correctTracker[0]
    correctApplication = Application.query.filter_by(application_id=app_id).all()
    if len(correctApplication) != 1:
        return render_template(
            "error.html",
            msg="Sorry, either zero or multiple applications exist with that id."
            " Please clean the dataset.",
        )
    correctApplication = correctApplication[0]
    return render_template(
        "application.html",
        title=correctApplication.company_name,
        application=correctApplication,
    )


@app.route("/trackers/add_new")
@register_breadcrumb(app, ".add_new", "Add New Tracker")
def addNewTracker():
    return "add New Tracker"


@app.route("/trackers/<tracker_name>/add_new")
@register_breadcrumb(app, ".tracker.add_new", "Add New Application")
def addNewApplication(tracker_name):
    return "add New Application"


@app.route("/trackers/<tracker_name>/<app_id>/add_new")
@register_breadcrumb(app, ".tracker.application.add_new", "Add New Event")
def addNewEvent(tracker_name, app_id):
    return "add New Event"
