from app import db, loginManager
from enum import Enum
import sqlalchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from typing import List


student_achievement = sqlalchemy.Table('student_achievement',
                                       db.metadata,
                                       sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True,
                                                         autoincrement=False),
                                       sqlalchemy.Column('student', sqlalchemy.Integer,
                                                         sqlalchemy.ForeignKey('student.id')),
                                       sqlalchemy.Column('achievement', sqlalchemy.Integer,
                                                         sqlalchemy.ForeignKey('achievement.id')))


class User(db.Model, UserMixin):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    authorization_code = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String(102), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), unique=True)
    type = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)  # 0 - student, 1 - parent, 2 - teacher, 3 - admin

    students = db.relationship('Student', backref='student_user_data', lazy='dynamic')
    mothers = db.relationship('Mother', backref='parent_user_data', lazy='dynamic')
    fathers = db.relationship('Father', backref='parent_user_data', lazy='dynamic')
    teachers = db.relationship('Teacher', backref='teacher_user_data', lazy='dynamic')
    admins = db.relationship('Admin', backref='admin_user_data', lazy='dynamic')

    def __init__(self, authorization_code, name, surename, password, user_type, email=None):
        self.authorization_code = authorization_code
        self.name = name
        self.surname = surename
        self.set_password(password)
        self.email = email
        self.type = user_type

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id


class Student(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=False)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("class.id"), nullable=False)
    mother_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("mother.id"))
    father_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("father.id"))
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)

    rates = orm.relationship("Rate", backref="student", lazy='dynamic')
    achievement = orm.relationship("Achievement", secondary=student_achievement, backref='students')

    def __init__(self, user_id, class_id=None):
        self.user_id = user_id
        self.class_id = class_id


class Mother(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))

    kids = db.relationship('Student', backref='mother', lazy='dynamic')

    def __init__(self, user_id):
        self.user_id = user_id


class Father(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))

    kids = db.relationship('Student', backref='father', lazy='dynamic')

    def __init__(self, user_id):
        self.user_id = user_id


class Teacher(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))

    lessons = orm.relationship('Lesson', backref='teacher', lazy='dynamic')

    def __init__(self, user_id):
        self.user_id = user_id


class Admin(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    school_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("school.id"))


class Subject(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)

    textbooks = orm.relationship('Textbook', backref='subject', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class Lesson(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subject.id"), nullable=False)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=45)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teacher.id"), nullable=False)
    cabinet = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("cabinet.id"), nullable=False)
    missing_students = sqlalchemy.Column(sqlalchemy.String(255))
    homework = sqlalchemy.Column(sqlalchemy.Text(1000))

    def __init__(self, subject_id, datetime, duration, teacher_id, cabinet):
        self.subject_id = subject_id
        self.datetime = datetime
        self.duration = duration
        self.teacher_id = teacher_id
        self.cabinet = cabinet


class Cabinet(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(32))

    def __init__(self, number):
        self.number = number


class Rate(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    rate = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("student.id"), nullable=False)
    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lesson.id"), nullable=False)

    def __init__(self, rate, student_id, lesson_id):
        self.rate = max(min(rate, 5), 2)
        self.student_id = student_id
        self.lesson_id = lesson_id


class Class(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    symbol = sqlalchemy.Column(sqlalchemy.String(1), nullable=False)
    class_manager_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teacher.id"), nullable=False)
    timetable_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("timetable.id"))
    students = orm.relationship('Student', backref='class', lazy='dynamic')

    def __init__(self, number, symbol, class_manager_id):
        self.number = max(min(number, 11), 1)
        self.symbol = symbol
        self.class_manager_id = class_manager_id


class School(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(120))

    admins = orm.relationship('Admin', backref='school', lazy='dynamic')

    def __init__(self, number, name=None):
        self.number = number
        self.name = name

    def __repr__(self):
        if self.name:
            return f"{self.name} №{self.number}"
        else:
            return f"{self.number}"


class Timetable(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Monday = sqlalchemy.Column(sqlalchemy.String(100))
    Tuesday = sqlalchemy.Column(sqlalchemy.String(100))
    Wednesday = sqlalchemy.Column(sqlalchemy.String(100))
    Thursday = sqlalchemy.Column(sqlalchemy.String(100))
    Friday = sqlalchemy.Column(sqlalchemy.String(100))
    Saturday = sqlalchemy.Column(sqlalchemy.String(100))
    Sunday = sqlalchemy.Column(sqlalchemy.String(100))

    class_id = orm.relationship('Class', backref='timetable', uselist=False)

    def __init__(self, list_of_the_days):
        self.Monday = list_of_the_days[0]
        self.Monday = list_of_the_days[1]
        self.Monday = list_of_the_days[2]
        self.Monday = list_of_the_days[3]
        self.Monday = list_of_the_days[4]
        if len(list_of_the_days) == 6:
            self.Saturday = list_of_the_days[5]


class TimetableLesson(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subject.id"), nullable=False)
    time = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=45)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teacher.id"), nullable=False)
    cabinet = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("cabinet.id"), nullable=False)

    def __init__(self, subject_id, time, duration, teacher_id, cabinet):
        self.subject_id = subject_id
        self.time = time
        self.duration = duration
        self.teacher_id = teacher_id
        self.cabinet = cabinet


class Textbook(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subject.id"), nullable=False)
    class_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)

    def __init__(self, subject_id, class_number, link):
        self.subject_id = subject_id
        self.class_number = max(min(class_number, 11), 1)
        self.link = link


class Achievement(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String(50))
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    def __init__(self, name, text=None, score=0):
        self.name = name
        self.text = text
        self.score = score


class NotLoggedUser(AnonymousUserMixin):
    username = "Sign In"


loginManager.anonymous_user = NotLoggedUser
