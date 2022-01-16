from flask import Blueprint
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from flask import render_template

main = Blueprint("main", __name__)
default_breadcrumb_root(main, ".")


@main.route("/")
@register_breadcrumb(main, ".", "Homepage")
def homepage():
    return render_template("homepage.html")
