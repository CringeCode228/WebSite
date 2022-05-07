import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, EmailField, IntegerField, \
    FieldList, FormField, SelectField, DateTimeField, TimeField, FileField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Class, Mother, Father


def get_class():
    return Class.query.all()


def get_mother():
    return Mother.query.all()


def get_father():
    return Father.query.all()


class AdminRegistrationForm(FlaskForm):
    authorization_code = IntegerField("Auth code", validators=[InputRequired()])
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
    class_id = QuerySelectField("Class", query_factory=get_class, validators=[Optional()])
    mother_id = QuerySelectField("Mother", query_factory=get_mother, validators=[Optional()])
    father_id = QuerySelectField("Father", query_factory=get_father, validators=[Optional()])
    score = IntegerField("Score")


class AdminUpdateStudentForm(AdminUpdateForm):
    class_id = QuerySelectField("Class", query_factory=get_class, validators=[Optional()])
    mother_id = QuerySelectField("Mother", query_factory=get_mother, validators=[Optional()])
    father_id = QuerySelectField("Father", query_factory=get_father, validators=[Optional()])
    score = IntegerField("Score", validators=[Optional()])


class AdminRegistrationParentForm(AdminRegistrationForm):
    type = RadioField("Пол", choices=[("mother", "Мама"), ("father", "Папа")])


class AdminUpdateParentForm(AdminUpdateForm):
    type = RadioField("Пол", choices=[("mother", "Мама"), ("father", "Папа")])


class AdminRegistrationClassForm(FlaskForm):
    number = IntegerField("Number")
    symbol = StringField("Letter")
    school_id = QuerySelectField("School")
    class_manager_id = QuerySelectField("Class manager")


class AdminUpdateClassForm(FlaskForm):
    number = IntegerField("Number")
    symbol = StringField("Letter")
    school_id = QuerySelectField("School")
    class_manager_id = QuerySelectField("Class manager")


class AdminRegistrationSubjectForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])


class AdminUpdateSubjectForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])


class AdminRegistrationLessonForm(FlaskForm):
    subject_id = QuerySelectField("Subject")
    datetime = DateTimeField("Date and Time")
    duration = IntegerField("Duration")
    teacher_id = QuerySelectField("Teacher")
    cabinet_id = QuerySelectField("Cabinet")


class AdminUpdateLessonForm(FlaskForm):
    subject_id = QuerySelectField("Subject")
    datetime = DateTimeField("Date and Time")
    duration = IntegerField("Duration")
    teacher_id = QuerySelectField("Teacher")
    cabinet_id = QuerySelectField("Cabinet")


class AdminRegistrationTimetableForm(FlaskForm):
    pass


class AdminUpdateTimetableForm(FlaskForm):
    pass


class AdminRegistrationCabinetForm(FlaskForm):
    number = IntegerField("Number")
    name = StringField("Name")


class AdminUpdateCabinetForm(FlaskForm):
    number = IntegerField("Number")
    name = StringField("Name")


class AdminRegistrationRateForm(FlaskForm):
    student_id = QuerySelectField("Student")
    rate = IntegerField("Rate")
    lesson_id = QuerySelectField("Lesson")


class AdminUpdateRateForm(FlaskForm):
    student_id = QuerySelectField("Student")
    rate = IntegerField("Rate")
    lesson_id = QuerySelectField("Lesson")


class AdminRegistrationTextbookForm(FlaskForm):
    subject_id = QuerySelectField("Subject")
    class_number = IntegerField("Class")
    link = FileField("Link to book")


class AdminUpdateTextbookForm(FlaskForm):
    subject_id = QuerySelectField("Subject")
    class_number = IntegerField("Class")
    link = FileField("Link to book")


class AdminRegistrationAchievementForm(FlaskForm):
    name = StringField("Title")
    text = StringField("Addition")
    score = IntegerField("Score")


class AdminUpdateAchievementForm(FlaskForm):
    name = StringField("Title")
    text = StringField("Addition")
    score = IntegerField("Score")


class LoginForm(FlaskForm):
    id_ = IntegerField("Login", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Submit")


class AuthorizationForm(FlaskForm):
    authorization_code = IntegerField("Activate code")
    submit = SubmitField("Submit")
