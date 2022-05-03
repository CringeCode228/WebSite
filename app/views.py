from app import application
from flask import render_template
from app import forms
from app import authorization
from app import admin_panel
from flask import request
from app import loginManager
from flask_login import login_required, current_user
from flask import redirect, url_for
from app import no_cache


@application.route("/index")
@application.route("/")
def index():
    return render_template("index.html", user=current_user)


@application.route("/simple_form", methods=['GET', 'POST'])
def simple_form():
    form = forms.SimpleForm()
    return render_template("simple_form.html", title="Simple form", form=form)


@application.errorhandler(404)
def error404(error):
    return render_template("error.html", error_text="Sorry, internal server error(",
                           error_image="images/error.png", user=current_user)


@application.errorhandler(500)
def error(error):
    return render_template("error.html", error_text="Sorry, internal server error(",
                           error_image="images/error.png", user=current_user)


@application.route("/search")
def search():
    return request.args.get("request")


@application.route("/login_only")
@login_required
def login_only():
    return "You login"


@loginManager.unauthorized_handler
def not_login():
    return redirect(url_for("login"))


@application.route("/students")
def students():
    return "students"
