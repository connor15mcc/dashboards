from flask import Blueprint
from flask_breadcrumbs import default_breadcrumb_root
from flask import render_template

manageAcct = Blueprint("manageAcct", __name__)
default_breadcrumb_root(manageAcct, ".")


@manageAcct.route("/login")
def root():
    return render_template("manageAcct/login.html")
