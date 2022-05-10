import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, TimeField, FileField, \
    RadioField, DateTimeLocalField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, Optional, NumberRange, Regexp
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from app.models import Class, Mother, Father, School, Teacher, Subject, Cabinet, Lesson, Student, User, Achievement
from functools import partial
from wtforms import ValidationError


def get_data(class_):
    return class_.query.all()


def check_resolution(resolution):
    def check_resolution_(form, field):
        if type(field) == FileField:
            if field.data.filename.split(".")[-1] != resolution:
                form.errors.update({"link": ValidationError(f"File must be '{resolution}' resolution")})

    return check_resolution_


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

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email must be unique")


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

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email must be unique")


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
    achievements = QuerySelectMultipleField("Achievements", query_factory=partial(get_data, Achievement),
                                            validators=[Optional()])


class AdminRegistrationParentForm(AdminRegistrationForm):
    type = RadioField("Пол", choices=[("mother", "Мама"), ("father", "Папа")])


class AdminUpdateParentForm(AdminUpdateForm):
    pass


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
    datetime = DateTimeLocalField("Date and Time", format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
    duration = IntegerField("Duration", validators=[InputRequired()])
    teacher_id = QuerySelectField("Teacher", query_factory=partial(get_data, Teacher), validators=[InputRequired()])
    cabinet_id = QuerySelectField("Cabinet", query_factory=partial(get_data, Cabinet), validators=[InputRequired()])
    class_id = QuerySelectField("Class", query_factory=partial(get_data, Class), validators=[Optional()])
    submit = SubmitField("Register")


class AdminUpdateLessonForm(FlaskForm):
    subject_id = QuerySelectField("Subject", query_factory=partial(get_data, Subject), validators=[Optional()])
    datetime = DateTimeLocalField("Date and Time", format="%Y-%m-%dT%H:%M", validators=[Optional()])
    duration = IntegerField("Duration", validators=[Optional()])
    teacher_id = QuerySelectField("Teacher", query_factory=partial(get_data, Teacher), validators=[Optional()])
    cabinet_id = QuerySelectField("Cabinet", query_factory=partial(get_data, Cabinet), validators=[Optional()])
    class_id = QuerySelectField("Class", query_factory=partial(get_data, Class), validators=[Optional()])
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

    def validate_link(self, field):
        if field.data.filename.split(".")[-1] != "pdf":
            raise ValidationError(f"File must be 'pdf' resolution")


class AdminUpdateTextbookForm(FlaskForm):
    subject_id = QuerySelectField("Subject", query_factory=partial(get_data, Subject), validators=[Optional()])
    class_number = IntegerField("Class", validators=[Optional()])
    link = FileField("Link to book", validators=[check_resolution('pdf'), Optional()])
    submit = SubmitField("Update")

    def validate_link(self, field):
        if field.data.filename.split(".")[-1] != "pdf":
            raise ValidationError(f"File must be 'pdf' resolution")


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


class AdminRegistrationSchoolForm(FlaskForm):
    number = IntegerField("Number", validators=[InputRequired()])
    name = StringField("Name", validators=[Optional()])
    submit = SubmitField("Register")


class AdminUpdateSchoolForm(FlaskForm):
    name = StringField("Name", validators=[Optional()])
    submit = SubmitField("Update")


class LoginForm(FlaskForm):
    id_ = IntegerField("Login", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Submit")


def student_score_trade_form(student):
    class StudentScoreTrade(FlaskForm):
        lesson_id = QuerySelectField("Выберите урок: ",
                                     query_factory=lambda:
                                     Lesson.query.filter(Lesson.lesson_class_data == student.student_class_data).all())
        submit = SubmitField("Обменять")
    score_trade = StudentScoreTrade()
    return score_trade


def teacher_lesson_form(lesson):
    class TeacherLessonForm(FlaskForm):
        homework = StringField("Home work", validators=[Length(-1, 999)])
        missing_students = QuerySelectMultipleField("Missing students",
                                                    query_factory=lambda: lesson.lesson_class_data.students)
        submit = SubmitField("Submit")

    lesson_form = TeacherLessonForm()
    return lesson_form


def teacher_rate_form(lesson):
    class TeacherRateForm(FlaskForm):
        rate = SelectField("Rate", choices=("2", "3", "4", "5"))
        student_id = QuerySelectField("Student", query_factory=lambda: lesson.lesson_class_data.students)
        lesson_id = lesson
        submit = SubmitField("Submit")

    rate_form = TeacherRateForm()
    return rate_form
