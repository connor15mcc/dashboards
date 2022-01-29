from flask import Blueprint, send_from_directory
from flask import redirect, url_for, render_template, flash, request
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from flask_login import current_user
from dashboards.appTracker.applications.forms import (
    EditNotes,
    NewApplication,
    EditApplication,
)
from dashboards.appTracker.events.routes import deleteEvent
from dashboards.models import Application, Tracker, Event
from dashboards.appTracker.filters.filters import to_name, hasCoverLetter
from dashboards import db, executor, login_manager
from datetime import datetime
import secrets
from resumes import render
import shutil
import os

applications = Blueprint("applications", __name__)
default_breadcrumb_root(applications, ".appTracker.tracker")


@applications.before_request
def restrict_applications_to_users():
    if not current_user.is_authenticated:
        return redirect(url_for(login_manager.login_view))


@applications.route("/<tracker_nameid>/")
@register_breadcrumb(applications, ".", "Tracker")
def oneTracker(tracker_nameid):
    trackerName = to_name(tracker_nameid)
    correctTracker = Tracker.query.filter_by(name=trackerName).first_or_404()
    return render_template(
        "appTracker/tracker.html",
        title="Application Tracker - " + correctTracker.name,
        tracker=correctTracker,
    )


@applications.route("/<tracker_nameid>/add_new", methods=["GET", "POST"])
@register_breadcrumb(applications, ".add_new", "Add New Application")
def addNewApplication(tracker_nameid):
    form = NewApplication()
    if form.validate_on_submit():
        correctTracker = Tracker.query.filter_by(
            name=to_name(tracker_nameid)
        ).first_or_404()
        coverletter_file = secrets.token_hex(10) + ".pdf"
        application = Application(
            company_name=form.company_name.data,
            position_name=form.position_name.data,
            source=form.source.data,
            link=form.link.data,
            status="Initialized",
            coverletter=coverletter_file,
            addr1=form.addr1.data,
            addr2=form.addr2.data,
            of_tracker=correctTracker.tracker_id,
        )
        executor.submit(createCoverLetter, coverletter_file, application)
        db.session.add(application)
        db.session.commit()
        firstHistory = Event(
            desc=f"Initialized application for {form.company_name.data}",
            from_me=True,
            action_necessary=True,
            date=datetime.now(),
            of_application=application.application_id,
        )
        db.session.add(firstHistory)
        db.session.commit()
        flash(f"New Application added for {form.company_name.data}!", "success")
        return redirect(
            url_for("applications.oneTracker", tracker_nameid=tracker_nameid)
        )
    return render_template(
        "appTracker/new_application.html",
        title="Application Tracker - " + "New Application",
        form=form,
    )


@applications.route("/<tracker_nameid>/<app_id>/edit", methods=["GET", "POST"])
@register_breadcrumb(applications, ".edit", "Edit Application")
def editApplication(tracker_nameid, app_id):
    currentApplication = Application.query.filter_by(
        application_id=app_id
    ).first_or_404()
    form = EditApplication()
    if form.validate_on_submit():
        deleteCoverLetter(currentApplication)
        coverletter_file = secrets.token_hex(10) + ".pdf"
        executor.submit(createCoverLetter, coverletter_file, currentApplication)
        currentApplication.company_name = form.company_name.data
        currentApplication.position_name = form.position_name.data
        currentApplication.source = form.source.data
        currentApplication.link = form.link.data
        currentApplication.status = form.status.data
        currentApplication.coverletter = coverletter_file
        currentApplication.addr1 = form.addr1.data
        currentApplication.addr2 = form.addr2.data
        db.session.commit()
        flash(
            f"Application for {currentApplication.company_name} has been updated!",
            "success",
        )
        return redirect(
            url_for("applications.oneTracker", tracker_nameid=tracker_nameid)
        )
    elif request.method == "GET":
        form.company_name.data = currentApplication.company_name
        form.position_name.data = currentApplication.position_name
        form.source.data = currentApplication.source
        form.link.data = currentApplication.link
        form.status.data = currentApplication.status
        form.addr1.data = currentApplication.addr1
        form.addr2.data = currentApplication.addr2
    return render_template(
        "appTracker/edit_application.html",
        title="Application Tracker - " + "Edit Application",
        form=form,
    )


@applications.route("/tracker/<tracker_nameid>/<app_id>/delete", methods=["GET"])
def deleteApplication(tracker_nameid, app_id):
    currentApplication = Application.query.filter_by(
        application_id=app_id
    ).first_or_404()
    deleteCoverLetter(currentApplication)
    for event in currentApplication.event_history:
        deleteEvent(tracker_nameid, app_id, event.event_id)
    db.session.delete(currentApplication)
    db.session.commit()
    flash("This application has been deleted", "success")
    return redirect(url_for("applications.oneTracker", tracker_nameid=tracker_nameid))


@applications.route(
    "/tracker/<tracker_nameid>/<app_id>/editNotes", methods=["GET", "POST"]
)
@register_breadcrumb(applications, ".editNotes", "Edit Notes")
def editNotes(tracker_nameid, app_id):
    currentApplication = Application.query.filter_by(
        application_id=app_id
    ).first_or_404()
    form = EditNotes()
    if form.validate_on_submit():
        currentApplication.notes = form.notes.data
        db.session.commit()
        flash(
            f"Notes for {currentApplication.company_name} has been updated!",
            "success",
        )
        return redirect(
            url_for(
                "events.oneApplication", tracker_nameid=tracker_nameid, app_id=app_id
            )
        )
    elif request.method == "GET":
        form.notes.data = currentApplication.notes
    return render_template(
        "appTracker/edit_notes.html",
        title="Application Tracker - " + "Edit Notes",
        form=form,
    )


@applications.route("/tracker/<tracker_nameid>/<app_id>/coverletter")
def viewCoverLetter(tracker_nameid, app_id):
    currentApplication = Application.query.filter_by(
        application_id=app_id
    ).first_or_404()
    if hasCoverLetter(currentApplication):
        return send_from_directory(
            directory="coverletters/",
            path=currentApplication.coverletter,
            as_attachment=True,
            attachment_filename=(
                f"coverletter_{currentApplication.company_name.lower()}.pdf"
            ),
        )
    else:
        return redirect(
            url_for(
                "applications.editApplication",
                tracker_nameid=tracker_nameid,
                app_id=app_id,
            )
        )


def createCoverLetter(path, app: Application):
    render.update_coverletter(app)
    shutil.move(
        os.path.join(os.path.dirname(__file__), "../../../resumes/coverletter.pdf"),
        os.path.join(os.path.dirname(__file__), f"../../coverletters/{path}"),
    )


def deleteCoverLetter(app):
    try:
        os.remove(
            os.path.join(
                os.path.dirname(__file__),
                f"../../coverletters/{app.coverletter}",
            )
        )
    finally:
        return


@applications.route("/tracker/<tracker_nameid>/resume")
def viewResume(tracker_nameid):
    return send_from_directory(
        directory="../resumes/",
        path="resume.pdf",
        as_attachment=True,
    )
