from flask import Blueprint
from flask_breadcrumbs import default_breadcrumb_root
from flask import render_template

main = Blueprint("main", __name__)
default_breadcrumb_root(main, ".")


@main.route("/")
def root():
    return render_template("homepage.html")
