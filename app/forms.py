from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, EmailField, IntegerField, \
    FieldList, FormField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import School


def school_query():
    return School.query.all()


class SimpleForm(FlaskForm):
    simpleField = TextAreaField("Simple text")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=32)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[DataRequired(), Length(max=32)],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    authorization_code = IntegerField("Auth code", validators=[InputRequired()])
    name = StringField("Username", validators=[InputRequired(), Length(max=32)],
                           render_kw={"placeholder": "Username"})
    surename = StringField("Username", validators=[InputRequired(), Length(max=32)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(max=32),
                                                     EqualTo("password_check", message="Passwords must match")],
                             render_kw={"placeholder": "Password"})
    password_check = PasswordField("Password", validators=[InputRequired(), Length(max=32)],
                                   render_kw={"placeholder": "Confirm password"})
    email = EmailField("Email", validators=[InputRequired(), Length(max=256), Email()],
                       render_kw={"placeholder": "Email"})
    submit = SubmitField("Sign In")


class NewStudentForm(RegistrationForm):
    school_id = QuerySelectField("School", query_factory=school_query)
