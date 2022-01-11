from flask import Blueprint
from flask import redirect, url_for, render_template, flash, request
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from tracker.events.forms import NewEvent, EditEvent
from tracker.events.utils import updateStatus
from tracker.models import Application, Event
from tracker.filters.filters import format_datetime
from tracker import db


events = Blueprint("events", __name__)
default_breadcrumb_root(events, ".")


@events.route("/trackers/<tracker_nameid>/<app_id>")
@register_breadcrumb(
    events,
    ".tracker.application",
    "Application",
)
def oneApplication(tracker_nameid, app_id):
    correctApplication = Application.query.filter_by(
        application_id=app_id
    ).first_or_404()
    return render_template(
        "application.html",
        title=correctApplication.company_name,
        application=correctApplication,
    )


@events.route("/trackers/<tracker_nameid>/<app_id>/add_new", methods=["GET", "POST"])
@register_breadcrumb(events, ".tracker.application.add_new", "Add New Event")
def addNewEvent(tracker_nameid, app_id):
    form = NewEvent()
    print(type(form.date.data))
    if form.validate_on_submit():
        correctApplication = Application.query.filter_by(
            application_id=app_id
        ).first_or_404()
        event = Event(
            desc=form.desc.data,
            from_me=form.from_me.data,
            action_necessary=form.action_necessary.data,
            date=form.date.data,
            of_application=correctApplication.application_id,
        )
        updateStatus(correctApplication, form.desc.data)
        db.session.add(event)
        db.session.commit()
        flash(f"New Event added for {format_datetime(form.date.data)}!", "success")
        return redirect(
            url_for(
                "events.oneApplication", tracker_nameid=tracker_nameid, app_id=app_id
            )
        )
    return render_template("new_event.html", title="New Event", form=form)


@events.route("/tracker/<tracker_nameid>/<app_id>/<event_id>", methods=["GET", "POST"])
@register_breadcrumb(events, ".tracker.application.edit", "Edit Event")
def editEvent(tracker_nameid, app_id, event_id):
    currentEvent = Event.query.filter_by(event_id=event_id).first_or_404()
    form = EditEvent()
    if form.validate_on_submit():
        correctApplication = Application.query.filter_by(
            application_id=app_id
        ).first_or_404()
        updateStatus(correctApplication, form.desc.data)
        db.session.commit()

        currentEvent.desc = form.desc.data
        currentEvent.from_me = form.from_me.data
        currentEvent.action_necessary = form.action_necessary.data
        currentEvent.date = form.date.data
        db.session.commit()
        flash(
            f"Event with {currentEvent.desc} has been updated!",
            "success",
        )
        return redirect(
            url_for(
                "events.oneApplication", tracker_nameid=tracker_nameid, app_id=app_id
            )
        )
    elif request.method == "GET":
        form.desc.data = currentEvent.desc
        form.from_me.data = currentEvent.from_me
        form.action_necessary.data = currentEvent.action_necessary
        form.date.data = currentEvent.date
    return render_template("edit_event.html", title="Edit Event", form=form)


@events.route("/tracker/<tracker_nameid>/<app_id>/<event_id>/delete", methods=["GET"])
def deleteEvent(tracker_nameid, app_id, event_id):
    currentEvent = Event.query.filter_by(event_id=event_id).first_or_404()
    db.session.delete(currentEvent)
    db.session.commit()
    flash("This event has been deleted", "success")
    return redirect(
        url_for("events.oneApplication", tracker_nameid=tracker_nameid, app_id=app_id)
    )