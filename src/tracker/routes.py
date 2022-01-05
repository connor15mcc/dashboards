from flask import redirect, url_for, render_template, flash, request, session
from flask_breadcrumbs import register_breadcrumb
from tracker import app, db
from tracker.models import Tracker, Application, Event
from tracker.forms import (
    NewApplication,
    NewTracker,
    NewEvent,
    EditApplication,
    EditTracker,
    EditEvent,
)


@app.route("/")
def root():
    return redirect(url_for("allTrackers"))


@app.route("/trackers/")
@register_breadcrumb(app, ".", "Home")
def allTrackers():
    return render_template(
        "trackers.html", title="Trackers", trackers=Tracker.query.all()
    )


@app.route("/trackers/<tracker_nameid>/")
@register_breadcrumb(app, ".tracker", "Tracker")
def oneTracker(tracker_nameid):
    trackerName = to_name(tracker_nameid)
    (correctTracker,) = Tracker.query.filter_by(name=trackerName).all()
    return render_template(
        "tracker.html",
        title=correctTracker.name,
        tracker=correctTracker,
    )


@app.route("/trackers/<tracker_nameid>/<app_id>")
@register_breadcrumb(
    app,
    ".tracker.application",
    "Application",
)
def oneApplication(tracker_nameid, app_id):
    (correctApplication,) = Application.query.filter_by(application_id=app_id).all()
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
        tracker = Tracker(name=to_name(to_nameid(form.name.data)), desc=form.desc.data)
        db.session.add(tracker)
        db.session.commit()
        flash(f"New Tracker added for {tracker.name}!", "success")
        return redirect(url_for("allTrackers"))
    return render_template("new_tracker.html", title="New Tracker", form=form)


@app.route("/trackers/<tracker_nameid>/add_new", methods=["GET", "POST"])
@register_breadcrumb(app, ".tracker.add_new", "Add New Application")
def addNewApplication(tracker_nameid):
    form = NewApplication()
    if form.validate_on_submit():
        (correctTracker,) = Tracker.query.filter_by(name=to_name(tracker_nameid)).all()
        application = Application(
            company_name=form.company_name.data,
            position_name=form.position_name.data,
            of_tracker=correctTracker.tracker_id,
        )
        db.session.add(application)
        db.session.commit()
        flash(f"New Application added for {form.company_name.data}!", "success")
        return redirect(url_for("oneTracker", tracker_nameid=tracker_nameid))
    return render_template("new_application.html", title="New Application", form=form)


@app.route("/trackers/<tracker_nameid>/<app_id>/add_new", methods=["GET", "POST"])
@register_breadcrumb(app, ".tracker.application.add_new", "Add New Event")
def addNewEvent(tracker_nameid, app_id):
    form = NewEvent()
    if form.validate_on_submit():
        (correctApplication,) = Application.query.filter_by(application_id=app_id).all()
        event = Event(
            desc=form.desc.data,
            from_me=form.from_me.data,
            date=form.date.data,
            of_application=correctApplication.application_id,
        )
        db.session.add(event)
        db.session.commit()
        flash(f"New Event added for {format_datetime(form.date.data)}!", "success")
        return redirect(
            url_for("oneApplication", tracker_nameid=tracker_nameid, app_id=app_id)
        )
    return render_template("new_event.html", title="New Event", form=form)


@app.route("/trackers/<tracker_nameid>/edit", methods=["GET", "POST"])
@register_breadcrumb(app, ".edit", "Edit Tracker")
def editTracker(tracker_nameid):
    (currentTracker,) = Tracker.query.filter_by(name=to_name(tracker_nameid)).all()
    form = EditTracker()
    if form.validate_on_submit():
        currentTracker.name = to_name(to_nameid(form.name.data))
        currentTracker.desc = form.desc.data
        db.session.commit()
        flash(f"Tracker {currentTracker.name} has been updated!", "success")
        return redirect(url_for("allTrackers"))
    elif request.method == "GET":
        form.name.data = currentTracker.name
        form.desc.data = currentTracker.desc
    return render_template("edit_tracker.html", title="Edit Tracker", form=form)


@app.route("/trackers/<tracker_nameid>/<app_id>/edit", methods=["GET", "POST"])
@register_breadcrumb(app, ".tracker.edit", "Edit Application")
def editApplication(tracker_nameid, app_id):
    (currentApplication,) = Application.query.filter_by(application_id=app_id).all()
    form = EditApplication()
    if form.validate_on_submit():
        currentApplication.company_name = form.company_name.data
        currentApplication.position_name = form.position_name.data
        db.session.commit()
        flash(
            f"Application for {currentApplication.company_name} has been updated!",
            "success",
        )
        return redirect(url_for("oneTracker", tracker_nameid=tracker_nameid))
    elif request.method == "GET":
        form.company_name.data = currentApplication.company_name
        form.position_name.data = currentApplication.position_name
    return render_template("edit_application.html", title="Edit Application", form=form)


@app.route("/tracker/<tracker_nameid>/<app_id>/<event_id>", methods=["GET", "POST"])
@register_breadcrumb(app, ".tracker.application.edit", "Edit Event")
def editEvent(tracker_nameid, app_id, event_id):
    (currentEvent,) = Event.query.filter_by(event_id=event_id).all()
    form = EditEvent()
    if form.validate_on_submit():
        currentEvent.desc = form.desc.data
        currentEvent.from_me = form.from_me.data
        currentEvent.date = form.date.data
        db.session.commit()
        flash(
            f"Event with {currentEvent.desc} has been updated!",
            "success",
        )
        return redirect(
            url_for("oneApplication", tracker_nameid=tracker_nameid, app_id=app_id)
        )
    elif request.method == "GET":
        form.desc.data = currentEvent.desc
        form.from_me.data = currentEvent.from_me
        form.date.data = currentEvent.date
    return render_template("edit_event.html", title="Edit Event", form=form)


@app.route("/tracker/<tracker_nameid>/delete", methods=["GET"])
def deleteTracker(tracker_nameid):
    (currentTracker,) = Tracker.query.filter_by(name=to_name(tracker_nameid)).all()
    for application in currentTracker.applications:
        deleteApplication(tracker_nameid, application.application_id)
    session["_flashes"].clear()
    db.session.delete(currentTracker)
    db.session.commit()
    flash("This tracker has been deleted", "success")
    return redirect(url_for("allTrackers"))


@app.route("/tracker/<tracker_nameid>/<app_id>/delete", methods=["GET"])
def deleteApplication(tracker_nameid, app_id):
    (currentApplication,) = Application.query.filter_by(application_id=app_id).all()
    for event in currentApplication.event_history:
        deleteEvent(tracker_nameid, app_id, event.event_id)
    session["_flashes"].clear()
    db.session.delete(currentApplication)
    db.session.commit()
    flash("This application has been deleted", "success")
    return redirect(url_for("oneTracker", tracker_nameid=tracker_nameid))


@app.route("/tracker/<tracker_nameid>/<app_id>/<event_id>/delete", methods=["GET"])
def deleteEvent(tracker_nameid, app_id, event_id):
    (currentEvent,) = Event.query.filter_by(event_id=event_id).all()
    db.session.delete(currentEvent)
    db.session.commit()
    flash("This event has been deleted", "success")
    return redirect(
        url_for("oneApplication", tracker_nameid=tracker_nameid, app_id=app_id)
    )


# Formatting Datetimes in Jinja:
@app.template_filter("formatdatetime")
def format_datetime(value, format="%B %d, %Y"):
    """Format a date time to (Default): Month Day, LongYear"""
    if value is None:
        return ""
    return value.strftime(format).lstrip("0").replace(" 0", " ")


# Transforming Tracker Names to IDs and Vice Versa:
@app.template_filter("to_nameid")
def to_nameid(name: str) -> str:
    return name.replace(" ", "_").lower()


@app.template_filter("to_name")
def to_name(nameid: str) -> str:
    parts = nameid.replace("_", " ").split(" ")
    return " ".join([word.capitalize() for word in parts])


@app.template_filter("to_nameid_from_trackerid")
def to_nameid_from_trackerid(trackerid: int) -> str:
    (correctTracker,) = Tracker.query.filter_by(tracker_id=trackerid)
    return to_nameid(correctTracker.name)
