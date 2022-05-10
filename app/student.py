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
from app.models import Lesson, Student, Rate, Achievement, Subject
from sqlalchemy.orm import joinedload


days = {0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"}


def get_self():
    return Student.query.filter_by(user_id=current_user.id_).first()


@application.route("/students/me/timetable/<int:year>/<int:month>/<int:day>")
@roles_required(Role.Student)
def student_timetable(year, month, day):
    try:
        t = datetime(year, month, day)
    except ValueError:
        return redirect(url_for("index"))
    student = get_self()
    lessons = Lesson.query.filter(Lesson.datetime > t,
                                  Lesson.datetime < t + timedelta(days=1),
                                  Lesson.lesson_class_data == student.student_class_data).all()
    return render_template("students/timetable.html", lessons=lessons, weekday=days[t.weekday()], url=request.url,
                           delta=timedelta)


@application.route("/students/me/timetable/<int:year>/<int:month>/<int:day>/previous")
@roles_required(Role.Student)
def student_timetable_previous(year, month, day):
    try:
        t = datetime(year, month, day) - timedelta(days=1)
    except ValueError:
        return redirect(url_for("index"))
    return redirect(url_for("student_timetable", year=t.year, month=t.month, day=t.day))


@application.route("/students/me/timetable/<int:year>/<int:month>/<int:day>/next")
@roles_required(Role.Student)
def student_timetable_next(year, month, day):
    try:
        t = datetime(year, month, day) + timedelta(days=1)
    except ValueError:
        return redirect(url_for("index"))
    return redirect(url_for("student_timetable", year=t.year, month=t.month, day=t.day))


@application.route("/students/me/timetable/today")
@roles_required(Role.Student)
def student_timetable_today():
    t = datetime.today()
    return redirect(url_for("student_timetable", year=t.year, month=t.month, day=t.day))


@application.route("/students/me/profile")
@roles_required(Role.Student)
def student_profile():
    return render_template("students/profile.html", student=get_self(), len=len)


@application.route("/students/me/rates")
@roles_required(Role.Student)
def student_rates():
    # rates = Rate.query.join(Lesson).join(Rate).order_by(Rate.lesson.datetime).all()
    rates = Rate.query.filter_by(student=get_self()).all()
    rates_group = {}
    rates = sorted(rates, key=lambda x: x.lesson.datetime)
    for rate in rates:
        if rate.lesson.subject.name not in rates_group:
            rates_group[rate.lesson.subject.name] = []
        rates_group[rate.lesson.subject.name].append(rate)
    return render_template("students/rates.html", rates=rates_group, len=len, round=round)


@application.route("/students/me/achievements")
@roles_required(Role.Student)
def student_achievements():
    return render_template("students/achievements.html", achievements=get_self().achievements)
