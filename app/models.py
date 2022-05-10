from app import db, loginManager
from enum import Enum
import sqlalchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from typing import List
from app.roles import Role


student_achievement = sqlalchemy.Table('student_achievement',
                                       db.metadata,
                                       sqlalchemy.Column('id_', sqlalchemy.Integer, primary_key=True,
                                                         autoincrement=True),
                                       sqlalchemy.Column('student', sqlalchemy.Integer,
                                                         sqlalchemy.ForeignKey('student.id_')),
                                       sqlalchemy.Column('achievement', sqlalchemy.Integer,
                                                         sqlalchemy.ForeignKey('achievement.id_')))


missing_students = sqlalchemy.Table('missing_students',
                                    db.metadata,
                                    sqlalchemy.Column('id_', sqlalchemy.Integer, primary_key=True,
                                                      autoincrement=True),
                                    sqlalchemy.Column('student', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey('student.id_')),
                                    sqlalchemy.Column('lesson', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey('lesson.id_')))


class User(db.Model, UserMixin):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String(102), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), unique=True)

    # 0 - student, 1 - mother, 2 - father, 3 - teachers, 4 - admin
    type = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    students = db.relationship('Student', backref='student_user_data', lazy='dynamic')
    mothers = db.relationship('Mother', backref='mother_user_data', lazy='dynamic')
    fathers = db.relationship('Father', backref='father_user_data', lazy='dynamic')
    teachers = db.relationship('Teacher', backref='teacher_user_data', lazy='dynamic')
    admins = db.relationship('Admin', backref='admin_user_data', lazy='dynamic')

    def __init__(self, name, surname, password, user_type, email=None):
        self.name = name
        self.surname = surname
        self.set_password(password)
        self.email = email
        self.type = user_type

    def __repr__(self):
        return "<User {} {}>".format(self.surname, self.name)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        print(self.password)
        print(password)
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id_

    def has_roles(self, *roles):
        if roles[0] == Role.Parent:
            if self.type == 1 or self.type == 2:
                return True
        elif int(roles[0]) == self.type:
            return True
        else:
            return False

    @staticmethod
    def get_user_by_token(token):
        return User.query.get(int(token))

    @staticmethod
    def email_confirmed_at():
        return True


class Student(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id_"), nullable=False)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("class.id_"))
    mother_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("mother.id_"))
    father_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("father.id_"))
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)

    rates = orm.relationship("Rate", backref="student", lazy='dynamic')
    achievements = orm.relationship("Achievement", secondary=student_achievement, backref='students')

    def __init__(self, user_id, class_id):
        self.user_id = user_id
        self.student_class_data = class_id

    def __repr__(self):
        return f"{self.student_user_data.name} {self.student_user_data.surname}"


class Mother(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id_"))

    kids = db.relationship('Student', backref='mother', lazy='dynamic')

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"{self.mother_user_data.surname} {self.mother_user_data.name}"


class Father(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id_"))

    kids = db.relationship('Student', backref='father', lazy='dynamic')

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"{self.father_user_data.surname} {self.father_user_data.name}"


class Teacher(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id_"))

    lessons = orm.relationship('Lesson', backref='teacher', lazy='dynamic')
    class_ = orm.relationship('Class', backref='manager', uselist=False)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"{self.teacher_user_data.surname} {self.teacher_user_data.name}"


class Admin(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id_"))
    # school_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("school.id_"))

    def __init__(self, user_id):
        self.user_id = user_id


class Subject(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)

    textbooks = orm.relationship('Textbook', backref='subject', lazy='dynamic')
    lessons = orm.relationship('Lesson', backref='subject', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Lesson(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subject.id_"), nullable=False)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=45)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("class.id_"))
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teacher.id_"))
    cabinet_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("cabinet.id_"))
    missing_students = orm.relationship("Student", secondary=missing_students, backref='missing_lessons')
    homework = sqlalchemy.Column(sqlalchemy.Text(1000))

    rates = orm.relationship("Rate", backref="lesson", lazy="dynamic")

    def __init__(self, subject_id, datetime, duration, teacher_id, cabinet_id, class_id):
        self.subject = subject_id
        self.datetime = datetime
        self.duration = duration
        self.teacher = teacher_id
        self.lesson_cabinet_data = cabinet_id
        self.lesson_class_data = class_id

    def __repr__(self):
        class_ = f"{self.lesson_class_data.number}{self.lesson_class_data.symbol}" if self.lesson_class_data \
            else "some class"
        return f"Lesson '{self.subject.name}' with {class_} at {self.datetime} in cabinet " \
               f"№{self.lesson_cabinet_data.number}"


class Cabinet(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(32))

    lessons = orm.relationship('Lesson', backref='lesson_cabinet_data', lazy='dynamic')

    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __repr__(self):
        if self.name:
            return f"{self.name} №{self.number}"
        else:
            return f"{self.number}"


class Rate(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    rate = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("student.id_"), nullable=False)
    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lesson.id_"), nullable=False)

    def __init__(self, rate, student_id, lesson_id):
        self.rate = rate
        self.student = student_id
        self.lesson = lesson_id

    def __repr__(self):
        return f"Rate {self.rate} by {self.student.student_user_data.name} {self.student.student_user_data.surname}" \
               f"at {self.lesson.subject.name}"


class Class(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    symbol = sqlalchemy.Column(sqlalchemy.String(1), nullable=False)
    class_manager_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teacher.id_"))
    timetable_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("timetable.id_"))
    school_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("school.id_"))

    students = orm.relationship('Student', backref='student_class_data', lazy='dynamic')
    lessons = orm.relationship('Lesson', backref='lesson_class_data', lazy='dynamic')

    def __init__(self, number, symbol, class_manager_id, school_id):
        self.number = number
        self.symbol = symbol
        self.manager = class_manager_id
        self.school = school_id

    def __repr__(self):
        return f"{self.number}{self.symbol} school №{self.school.number}"


class School(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(120))

    # admins = orm.relationship('Admin', backref='school', lazy='dynamic')
    classes = orm.relationship('Class', backref='school', lazy='dynamic')

    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __repr__(self):
        if self.name:
            return f"{self.name} №{self.number}"
        else:
            return f"{self.number}"


# Future content
class Timetable(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
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


# Future content
class TimetableLesson(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subject.id_"), nullable=False)
    time = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=45)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teacher.id_"), nullable=False)
    cabinet = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("cabinet.id_"), nullable=False)

    def __init__(self, subject_id, time, duration, teacher_id, cabinet):
        self.subject_id = subject_id
        self.time = time
        self.duration = duration
        self.teacher = teacher_id
        self.cabinet = cabinet


class Textbook(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subject.id_"), nullable=False)
    class_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)

    def __init__(self, subject, class_number, link):
        self.subject = subject
        self.class_number = max(min(class_number, 11), 1)
        self.link = link


class Achievement(db.Model):
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String(50))
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    def __init__(self, name, text=None, score=0):
        self.name = name
        self.text = text
        self.score = score

    def __repr__(self):
        return self.name


class NotLoggedUser(AnonymousUserMixin):
    username = "Sign In"


loginManager.anonymous_user = NotLoggedUser
