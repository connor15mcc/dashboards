from flask import Blueprint
from flask_breadcrumbs import default_breadcrumb_root
from flask_login import login_user, current_user, logout_user
from flask import render_template, redirect, url_for, request, flash
from dashboards import bcrypt
from dashboards.manageAcct.forms import LoginForm
from dashboards.models import User

manageAcct = Blueprint("manageAcct", __name__)
default_breadcrumb_root(manageAcct, ".")


@manageAcct.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page) if next_page else redirect(url_for("main.homepage"))
            )
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("manageAcct/login.html", title="Login", form=form)


@manageAcct.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.homepage"))
