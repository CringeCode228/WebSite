from app import application
from flask import render_template
from app.authorization import *
from app.admin_panel import *
from app.student import *
from app.parent import *
from app.teacher import *
from app import loginManager
from flask_login import current_user
from flask import redirect, url_for


@application.route("/index")
@application.route("/")
def index():
    return render_template("index.html", user=current_user)


@application.errorhandler(404)
def error404(error):
    return render_template("error.html", error_text="Sorry, page not found(",
                           error_image="images/error.png", user=current_user)


@application.errorhandler(500)
def error(error):
    return render_template("error.html", error_text="Sorry, internal server error(",
                           error_image="images/error.png", user=current_user)


@loginManager.unauthorized_handler
def not_login():
    return redirect(url_for("login"))
