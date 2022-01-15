from flask import Blueprint
from flask_breadcrumbs import default_breadcrumb_root
from flask import redirect, url_for

main = Blueprint("main", __name__)
default_breadcrumb_root(main, ".")


@main.route("/")
def root():
    return redirect(url_for("application-tracker.trackers.allTrackers"))
