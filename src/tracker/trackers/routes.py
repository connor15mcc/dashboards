from flask import Blueprint
from flask import redirect, url_for, render_template, flash, request, session
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from tracker.trackers.forms import NewTracker, EditTracker
from tracker.applications.routes import deleteApplication
from tracker.models import Tracker
from tracker.filters.filters import to_name, to_nameid
from tracker import db

trackers = Blueprint("trackers", __name__)
default_breadcrumb_root(trackers, ".")


@trackers.route("/trackers/")
@register_breadcrumb(trackers, ".", "Home")
def allTrackers():
    return render_template(
        "trackers.html", title="Trackers", trackers=Tracker.query.all()
    )


@trackers.route("/trackers/add_new", methods=["GET", "POST"])
@register_breadcrumb(trackers, ".add_new", "Add New Tracker")
def addNewTracker():
    form = NewTracker()
    if form.validate_on_submit():
        tracker = Tracker(name=to_name(to_nameid(form.name.data)), desc=form.desc.data)
        db.session.add(tracker)
        db.session.commit()
        flash(f"New Tracker added for {tracker.name}!", "success")
        return redirect(url_for("trackers.allTrackers"))
    return render_template("new_tracker.html", title="New Tracker", form=form)


@trackers.route("/trackers/<tracker_nameid>/edit", methods=["GET", "POST"])
@register_breadcrumb(trackers, ".edit", "Edit Tracker")
def editTracker(tracker_nameid):
    currentTracker = Tracker.query.filter_by(
        name=to_name(tracker_nameid)
    ).first_or_404()
    form = EditTracker()
    if form.validate_on_submit():
        currentTracker.name = to_name(to_nameid(form.name.data))
        currentTracker.desc = form.desc.data
        db.session.commit()
        flash(f"Tracker {currentTracker.name} has been updated!", "success")
        return redirect(url_for("trackers.allTrackers"))
    elif request.method == "GET":
        form.name.data = currentTracker.name
        form.desc.data = currentTracker.desc
    return render_template("edit_tracker.html", title="Edit Tracker", form=form)


@trackers.route("/tracker/<tracker_nameid>/delete", methods=["GET"])
def deleteTracker(tracker_nameid):
    currentTracker = Tracker.query.filter_by(
        name=to_name(tracker_nameid)
    ).first_or_404()
    for application in currentTracker.applications:
        deleteApplication(tracker_nameid, application.application_id)
    session["_flashes"].clear()
    db.session.delete(currentTracker)
    db.session.commit()
    flash("This tracker has been deleted", "success")
    return redirect(url_for("trackers.allTrackers"))
