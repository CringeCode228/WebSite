from app import application
from app import loginManager
from app import models
from flask import render_template, flash, redirect, url_for
from app import forms
from flask_login import current_user, login_user, logout_user
from app import models
from app import db
from werkzeug.security import generate_password_hash
import random
from flask_login import login_required
from app import no_cache
from app.forms import NewStudentForm

from app.models import Student


@application.route("/admin_panel/")
def admin_panel():
    return render_template("admin/index.html")


@application.route("/admin_panel/students")
def admin_panel_students():
    return render_template("admin/students.html", students=Student.query.all())


@application.route("/admin_panel/parents")
def admin_panel_parents():
    return "Page"


@application.route("/admin_panel/teachers")
def admin_panel_teachers():
    return "Page"


@application.route("/admin_panel/classes")
def admin_panel_classes():
    return "Page"


@application.route("/admin_panel/subjects")
def admin_panel_subjects():
    return "Page"


@application.route("/admin_panel/lessons")
def admin_panel_lessons():
    return "Page"


@application.route("/admin_panel/timetable")
def admin_panel_timetable():
    return "Page"


@application.route("/admin_panel/cabinets")
def admin_panel_cabinets():
    return "Page"


@application.route("/admin_panel/rates")
def admin_panel_rates():
    return "Page"


@application.route("/admin_panel/textbooks")
def admin_panel_textbooks():
    return "Page"


@application.route("/admin_panel/achievements")
def admin_panel_achievements():
    return "Page"


@application.route("/admin_panel/students/new", methods=["GET", "POST"])
def admin_panel_students_new():
    form = forms.NewStudentForm()
    if form.validate_on_submit():
        user = models.User(form.authorization_code.data, form.name.data, form.surename.data, form.password.data, 0,
                           form.email.data)
        db.session.add(user)
        db.session.commot()
        student = models.Student(user.id)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('admin_panel_students'))
    return render_template("admin/students.html", students=Student.query.all(), form=NewStudentForm())
