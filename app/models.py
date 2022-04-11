from app import db, loginManager
from enum import Enum
import sqlalchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm


class User(db.Model, UserMixin):

    __mapper_args__ = {'polymorphic_identity': 'user'}
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    authorization_code = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String(102), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(256), unique=True)

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


class Student(User):
    __mapper_args__ = {'polymorphic_identity': 'student'}
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), primary_key=True)
    user = orm.relationship("user")


class Parent(User):
    __mapper_args__ = {'polymorphic_identity': 'parent'}
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), primary_key=True)
    user = orm.relationship("user")


class Teacher(User):
    __mapper_args__ = {'polymorphic_identity': 'teacher'}
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), primary_key=True)
    user = orm.relationship("user")


class Admin(User):
    __mapper_args__ = {'polymorphic_identity': 'admin'}
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), primary_key=True)
    user = orm.relationship("user")


class Subject(db.Model):
    name = sqlalchemy.Column(sqlalchemy.String(32), primary_key=True)


class Lesson(db.Model):
    subject = sqlalchemy.Column(sqlalchemy.String(32), primary_key=True)


class Rate(db.Model):
    rate = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.CheckConstraint("rate>=2"),
                             sqlalchemy.CheckConstraint("rate<=5"))
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("student.id"))
    student = orm.relationship("student")


class SchoolClass(db.Model):
    number = sqlalchemy.Column(sqlalchemy.Integer)
    symbol = sqlalchemy.Column(sqlalchemy.String(1))
    class_manager_id = sqlalchemy.Column()


class Day(db.Model):
    pass


class School(db.Model):
    number = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String(120))


class NotLoggedUser(AnonymousUserMixin):
    username = "Sign In"


loginManager.anonymous_user = NotLoggedUser
