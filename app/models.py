from app import db, loginManager
from enum import Enum
import sqlalchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(Enum):
    default = 0
    moderator = 1
    admin = 2


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(102))
    email = db.Column(db.String(256), unique=True)
    role = db.Column(db.Enum(Role))

    def __init__(self, username, password, email, role):
        self.username = username
        self.set_password(password)
        self.email = email
        self.role = role

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id


class Student(User):
    pass


class Parent(User):
    pass


class Teacher(User):
    pass


class Admin(User):
    pass


class NotLoggedUser(AnonymousUserMixin):
    username = "Sign In"


loginManager.anonymous_user = NotLoggedUser
