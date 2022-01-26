from flask import Blueprint
from flask import redirect, url_for, render_template, flash, request, session
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from flask_login import current_user
from dashboards.appTracker.trackers.forms import NewTracker, EditTracker
from dashboards.appTracker.applications.routes import deleteApplication
from dashboards.models import Tracker
from dashboards.appTracker.filters.filters import to_name, to_nameid
from dashboards import db, login_manager


trackers = Blueprint("trackers", __name__)
default_breadcrumb_root(trackers, ".appTracker")


@trackers.before_request
def restrict_trackers_to_users():
    if not current_user.is_authenticated:
        return redirect(url_for(login_manager.login_view))


@trackers.route("/")
@register_breadcrumb(trackers, ".", "Trackers")
def allTrackers():
    return render_template(
        "appTracker/trackers.html",
        title="Application Tracker - " + "Trackers",
        trackers=Tracker.query.all(),
    )


@trackers.route("/add_new", methods=["GET", "POST"])
@register_breadcrumb(trackers, ".add_new", "Add New Tracker")
def addNewTracker():
    form = NewTracker()
    if form.validate_on_submit():
        tracker = Tracker(name=to_name(to_nameid(form.name.data)), desc=form.desc.data)
        db.session.add(tracker)
        db.session.commit()
        flash(f"New Tracker added for {tracker.name}!", "success")
        return redirect(url_for("trackers.allTrackers"))
    return render_template(
        "appTracker/new_tracker.html",
        title="Application Tracker - " + "New Tracker",
        form=form,
    )


@trackers.route("/<tracker_nameid>/edit", methods=["GET", "POST"])
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
    return render_template(
        "appTracker/edit_tracker.html",
        title="Application Tracker - " + "Edit Tracker",
        form=form,
    )


@trackers.route("/tracker/<tracker_nameid>/delete", methods=["GET"])
def deleteTracker(tracker_nameid):
    currentTracker = Tracker.query.filter_by(
        name=to_name(tracker_nameid)
    ).first_or_404()
    for application in currentTracker.applications:
        deleteApplication(tracker_nameid, application.application_id)
    db.session.delete(currentTracker)
    db.session.commit()
    flash("This tracker has been deleted", "success")
    return redirect(url_for("trackers.allTrackers"))
