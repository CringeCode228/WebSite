from app import application
from app import loginManager
from flask import render_template, redirect, url_for
from app import forms
from flask_login import current_user, login_user, logout_user
from app import models
from app import db
from werkzeug.security import generate_password_hash
from flask_login import login_required
from flask import request
from flask_user import roles_required
from flask_login import current_user
from flask import abort, send_from_directory
from app.roles import Role
from werkzeug.utils import secure_filename
from app.config import UPLOAD_FOLDER
import os
from flask import flash
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import Lesson, Teacher, Rate, Achievement, Subject, Teacher
from sqlalchemy.orm import joinedload
from app.forms import teacher_lesson_form, teacher_rate_form


days = {0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"}


def set_field(new_value, old_value):
    if new_value:
        return new_value
    else:
        return old_value


def get_self():
    return Teacher.query.filter_by(user_id=current_user.id_).first()


@application.route("/teachers/me/timetable/<int:year>/<int:month>/<int:day>")
@roles_required(Role.Teacher)
def teacher_timetable(year, month, day):
    try:
        t = datetime(year, month, day)
    except ValueError:
        return abort(404)
    teacher = get_self()
    lessons = Lesson.query.filter(Lesson.datetime > t,
                                  Lesson.datetime < t + timedelta(days=1),
                                  Lesson.teacher == teacher).all()
    return render_template("teachers/timetable.html", lessons=lessons, weekday=days[t.weekday()], url=request.url,
                           delta=timedelta)


@application.route("/teachers/me/timetable/<int:year>/<int:month>/<int:day>/previous")
@roles_required(Role.Teacher)
def teacher_timetable_previous(year, month, day):
    try:
        t = datetime(year, month, day) - timedelta(days=1)
    except ValueError:
        return redirect(url_for("index"))
    return redirect(url_for("teacher_timetable", year=t.year, month=t.month, day=t.day))


@application.route("/teachers/me/timetable/<int:year>/<int:month>/<int:day>/next")
@roles_required(Role.Teacher)
def teacher_timetable_next(year, month, day):
    try:
        t = datetime(year, month, day) + timedelta(days=1)
    except ValueError:
        return redirect(url_for("index"))
    return redirect(url_for("teacher_timetable", year=t.year, month=t.month, day=t.day))


@application.route("/teachers/me/timetable/today")
@roles_required(Role.Teacher)
def teacher_timetable_today():
    t = datetime.today()
    return redirect(url_for("teacher_timetable", year=t.year, month=t.month, day=t.day))


@application.route("/teachers/me/profile")
@roles_required(Role.Teacher)
def teacher_profile():
    return render_template("teachers/profile.html", teacher=get_self())


@application.route("/teachers/me/lessons/<int:id_>", methods=["GET", "POST"])
@roles_required(Role.Teacher)
def teacher_lesson(id_):
    lesson = Lesson.query.filter_by(id_=id_).first()
    if not lesson:
        return abort(404)
    form = teacher_lesson_form(lesson)
    if form.validate_on_submit():
        lesson.homework = set_field(form.homework.data, lesson.homework)
        lesson.missing_students.clear()
        lesson.missing_students.extend(form.missing_students.data)
        db.session.commit()
        return redirect(url_for("teacher_lesson", id_=id_))
    return render_template("teachers/lesson.html", lesson=lesson, form=form, delta=timedelta, Rate=Rate)


@application.route("/teachers/me/lessons/<int:id_>/set_rate", methods=["GET", "POST"])
@roles_required(Role.Teacher)
def teacher_set_rate(id_):
    lesson = Lesson.query.filter_by(id_=id_).first()
    if not lesson or lesson.teacher != get_self():
        return abort(404)
    form = teacher_rate_form(lesson)
    if form.validate_on_submit():
        rate = Rate(form.rate.data, form.student_id.data, form.lesson_id)
        db.session.add(rate)
        db.session.commit()
        return redirect(url_for("teacher_lesson", id_=id_))
    return render_template("teachers/set_rate.html", lesson=lesson, form=form, Rate=Rate)
