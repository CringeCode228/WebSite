import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, EmailField, IntegerField, \
    FieldList, FormField, SelectField, DateTimeField, TimeField, FileField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, Optional, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Class, Mother, Father, School, Teacher, Subject, Cabinet, Lesson, Student
from functools import partial


def get_data(class_):
    return class_.query.all()


# def get_classes():
#     return Class.query.all()
#
#
# def get_students():
#     return
#
#
# def get_mothers():
#     return Mother.query.all()
#
#
# def get_fathers():
#     return Father.query.all()
#
#
# def get_schools():
#     return School.query.all()
#
#
# def get_teachers():
#     return Teacher.query.all()
#
#
# def get_subjects():
#     return Subject.query.all()
#
#
# def get_cabinets():
#     return Cabinet.query.all()


class AdminRegistrationForm(FlaskForm):
    name = StringField("Username", validators=[InputRequired(), Length(max=32)],
                       render_kw={"placeholder": "Username"})
    surname = StringField("Username", validators=[InputRequired(), Length(max=32)],
                          render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(max=32),
                                                     EqualTo("password_check", message="Passwords must match")],
                             render_kw={"placeholder": "Password"})
    password_check = PasswordField("Password", validators=[InputRequired(), Length(max=32)],
                                   render_kw={"placeholder": "Confirm password"})
    email = EmailField("Email", validators=[InputRequired(), Length(max=256), Email()],
                       render_kw={"placeholder": "Email"})
    submit = SubmitField("Register")


class AdminUpdateForm(FlaskForm):
    name = StringField("Username", validators=[Length(max=32), Optional()],
                       render_kw={"placeholder": "Username"})
    surname = StringField("Username", validators=[Length(max=32), Optional()],
                          render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[Length(max=32),
                                                     EqualTo("password_check", message="Passwords must match"),
                                                     Optional()],
                             render_kw={"placeholder": "Password"})
    password_check = PasswordField("Password", validators=[Length(max=32), Optional()],
                                   render_kw={"placeholder": "Confirm password"})
    email = EmailField("Email", validators=[Length(max=256), Email(), Optional()],
                       render_kw={"placeholder": "Email"})
    submit = SubmitField("Update")


class AdminRegistrationStudentForm(AdminRegistrationForm):
    class_id = QuerySelectField("Class", query_factory=partial(get_data, Class), validators=[Optional()])
    mother_id = QuerySelectField("Mother", query_factory=partial(get_data, Mother), validators=[Optional()])
    father_id = QuerySelectField("Father", query_factory=partial(get_data, Father), validators=[Optional()])
    score = IntegerField("Score")


class AdminUpdateStudentForm(AdminUpdateForm):
    class_id = QuerySelectField("Class", query_factory=partial(get_data, Class), validators=[Optional()])
    mother_id = QuerySelectField("Mother", query_factory=partial(get_data, Mother), validators=[Optional()])
    father_id = QuerySelectField("Father", query_factory=partial(get_data, Father), validators=[Optional()])
    score = IntegerField("Score", validators=[Optional()])


class AdminRegistrationParentForm(AdminRegistrationForm):
    type = RadioField("Пол", choices=[("mother", "Мама"), ("father", "Папа")])


class AdminUpdateParentForm(AdminUpdateForm):
    type = RadioField("Пол", choices=[("mother", "Мама"), ("father", "Папа")], validators=[Optional()])


class AdminRegistrationClassForm(FlaskForm):
    number = IntegerField("Number", validators=[InputRequired()])
    symbol = StringField("Letter", validators=[InputRequired()])
    school_id = QuerySelectField("School", query_factory=partial(get_data, School), validators=[InputRequired()])
    class_manager_id = QuerySelectField("Class manager", query_factory=partial(get_data, Teacher),
                                        validators=[InputRequired()])
    submit = SubmitField("Register")


class AdminUpdateClassForm(FlaskForm):
    number = IntegerField("Number", validators=[Optional()])
    symbol = StringField("Letter", validators=[Optional()])
    school_id = QuerySelectField("School", query_factory=partial(get_data, School), validators=[Optional()])
    class_manager_id = QuerySelectField("Class manager", query_factory=partial(get_data, Teacher),
                                        validators=[Optional()])
    submit = SubmitField("Update")


class AdminRegistrationSubjectForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    submit = SubmitField("Register")


class AdminUpdateSubjectForm(FlaskForm):
    name = StringField("Name", validators=[Optional()])
    submit = SubmitField("Update")


class AdminRegistrationLessonForm(FlaskForm):
    subject_id = QuerySelectField("Subject", query_factory=partial(get_data, Subject), validators=[InputRequired()])
    datetime = DateTimeField("Date and Time", validators=[InputRequired()])
    duration = IntegerField("Duration", validators=[InputRequired()])
    teacher_id = QuerySelectField("Teacher", query_factory=partial(get_data, Teacher), validators=[InputRequired()])
    cabinet_id = QuerySelectField("Cabinet", query_factory=partial(get_data, Cabinet), validators=[InputRequired()])
    submit = SubmitField("Register")


class AdminUpdateLessonForm(FlaskForm):
    subject_id = QuerySelectField("Subject", query_factory=partial(get_data, Subject), validators=[Optional()])
    datetime = DateTimeField("Date and Time", validators=[Optional()])
    duration = IntegerField("Duration", validators=[Optional()])
    teacher_id = QuerySelectField("Teacher", query_factory=partial(get_data, Teacher), validators=[Optional()])
    cabinet_id = QuerySelectField("Cabinet", query_factory=partial(get_data, Cabinet), validators=[Optional()])
    submit = SubmitField("Update")


class AdminRegistrationTimetableForm(FlaskForm):
    pass


class AdminUpdateTimetableForm(FlaskForm):
    pass


class AdminRegistrationCabinetForm(FlaskForm):
    number = IntegerField("Number", validators=[InputRequired()])
    name = StringField("Name", validators=[Optional()])
    submit = SubmitField("Register")


class AdminUpdateCabinetForm(FlaskForm):
    number = IntegerField("Number", validators=[Optional()])
    name = StringField("Name", validators=[Optional()])
    submit = SubmitField("Update")


class AdminRegistrationRateForm(FlaskForm):
    student_id = QuerySelectField("Student", query_factory=partial(get_data, Student), validators=[InputRequired()])
    rate = IntegerField("Rate", validators=[InputRequired(), NumberRange(2, 5, "Rate must be a number from 2 to 5")])
    lesson_id = QuerySelectField("Lesson", query_factory=partial(get_data, Lesson), validators=[InputRequired()])
    submit = SubmitField("Register")


class AdminUpdateRateForm(FlaskForm):
    rate = IntegerField("Rate", validators=[Optional(), NumberRange(2, 5, "Rate must be a number from 2 to 5")])
    lesson_id = QuerySelectField("Lesson", query_factory=partial(get_data, Lesson), validators=[Optional()])
    submit = SubmitField("Update")


class AdminRegistrationTextbookForm(FlaskForm):
    subject_id = QuerySelectField("Subject", query_factory=partial(get_data, Subject), validators=[InputRequired()])
    class_number = IntegerField("Class", validators=[InputRequired()])
    link = FileField("Link to book", validators=[InputRequired()])
    submit = SubmitField("Register")


class AdminUpdateTextbookForm(FlaskForm):
    subject_id = QuerySelectField("Subject", query_factory=partial(get_data, Subject), validators=[Optional()])
    class_number = IntegerField("Class", validators=[Optional()])
    link = FileField("Link to book", validators=[Optional()])
    submit = SubmitField("Update")


class AdminRegistrationAchievementForm(FlaskForm):
    name = StringField("Title", validators=[InputRequired()])
    text = StringField("Addition", validators=[Optional()])
    score = IntegerField("Score", validators=[InputRequired()])
    submit = SubmitField("Register")


class AdminUpdateAchievementForm(FlaskForm):
    name = StringField("Title", validators=[Optional()])
    text = StringField("Addition", validators=[Optional()])
    score = IntegerField("Score", validators=[Optional()])
    submit = SubmitField("Update")


class LoginForm(FlaskForm):
    id_ = IntegerField("Login", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Submit")
