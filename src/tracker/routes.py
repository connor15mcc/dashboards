from flask import redirect, url_for, render_template, flash
from flask_breadcrumbs import register_breadcrumb
from tracker import app
from tracker.models import Tracker, Application
from tracker.forms import NewApplication, NewTracker, NewEvent


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


@app.route("/trackers/<tracker_name>/<app_id>")
@register_breadcrumb(
    app,
    ".tracker.application",
    "Application",
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


@app.route("/trackers/add_new", methods=["GET", "POST"])
@register_breadcrumb(app, ".add_new", "Add New Tracker")
def addNewTracker():
    form = NewTracker()
    if form.validate_on_submit():
        flash(f"New Tracker added for {form.name.data}!", "success")
        return redirect(url_for("allTrackers"))
    return render_template("new_tracker.html", title="New Tracker", form=form)


@app.route("/trackers/<tracker_name>/add_new", methods=["GET", "POST"])
@register_breadcrumb(app, ".tracker.add_new", "Add New Application")
def addNewApplication(tracker_name):
    form = NewApplication()
    if form.validate_on_submit():
        flash(f"New Application added for {form.company_name.data}!", "success")
        return redirect(url_for("oneTracker", tracker_name=tracker_name))
    return render_template("new_application.html", title="New Application", form=form)


@app.route("/trackers/<tracker_name>/<app_id>/add_new", methods=["GET", "POST"])
@register_breadcrumb(app, ".tracker.application.add_new", "Add New Event")
def addNewEvent(tracker_name, app_id):
    form = NewEvent()
    if form.validate_on_submit():
        flash(f"New Event added for {form.date.data:%B %d, %Y}!", "success")
        return redirect(
            url_for("oneApplication", tracker_name=tracker_name, app_id=app_id)
        )
    return render_template("new_event.html", title="New Appliction", form=form)


@app.route("/trackers/<tracker_name>/edit")
@register_breadcrumb(app, ".tracker.edit", "Edit Tracker")
def editTracker(tracker_name):
    return f"edit {tracker_name}"


@app.route("/trackers/<tracker_name>/<app_id>/edit")
@register_breadcrumb(app, ".tracker.application.edit", "Edit Application")
def editApplication(tracker_name, app_id):
    return f"edit {app_id}"


@app.route("/tracker/<tracker_name>/<app_id>/<event_id>")
@register_breadcrumb(app, ".tracker.application.event.edit", "Edit Event")
def editEvent(tracker_name, app_id, event_id):
    return f"edit {event_id}"


# Formatting Datetimes in Jinja:
@app.template_filter("formatdatetime")
def format_datetime(value, format="%B %d, %Y"):
    """Format a date time to (Default): Month Day, LongYear"""
    if value is None:
        return ""
    return value.strftime(format).lstrip("0").replace(" 0", " ")
