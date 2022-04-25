from app import db, loginManager
from enum import Enum
import sqlalchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm


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

    students = db.relationship('Student', backref='student_user_data', lazy='dynamic')
    parents = db.relationship('Parent', backref='parent_user_data', lazy='dynamic')
    teachers = db.relationship('Teacher', backref='teacher_user_data', lazy='dynamic')
    admins = db.relationship('Admin', backref='admin_user_data', lazy='dynamic')

    def __init__(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email

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
    mother_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("parent.id"))
    father_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("parent.id"))
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)

    rates = orm.relationship("Rate", backref="student", lazy='dynamic')
    achievement = orm.relationship("Achievement", secondary=student_achievement, backref='students')


class Parent(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))

    kids = db.relationship('Student', backref='parent', lazy='dynamic')


class Teacher(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))

    lessons = orm.relationship('Lesson', backref='teacher', lazy='dynamic')


class Admin(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    school_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("school.id"))


class Subject(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)

    textbooks = orm.relationship('Textbooks', backref='subject', lazy='dynamic')


class Lesson(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subject.id"), nullable=False)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=45)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teacher.id"), nullable=False)
    cabinet = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("cabinet.id"), nullable=False)
    missing_students = sqlalchemy.Column(sqlalchemy.String(255))
    homework = sqlalchemy.Column(sqlalchemy.Text(1000))


class Cabinet(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(32))


class Rate(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    rate = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("student.id"), nullable=False)
    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lesson.id"), nullable=False)


class Class(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    symbol = sqlalchemy.Column(sqlalchemy.String(1), nullable=False)
    class_manager_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teacher.id"), nullable=False)
    timetable_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("timetable.id"))


class School(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(120))

    admins = orm.relationship('Admin', backref='school', lazy='dynamic')


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


class TimetableLesson(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subject.id"), nullable=False)
    time = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=45)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teacher.id"), nullable=False)
    cabinet = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("cabinet.id"), nullable=False)


class Textbook(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subject.id"), nullable=False)
    class_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)


class Achievement(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String(50))
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


class NotLoggedUser(AnonymousUserMixin):
    username = "Sign In"


loginManager.anonymous_user = NotLoggedUser
