from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length


class SimpleForm(FlaskForm):
    simpleField = TextAreaField("Simple text")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=32)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[DataRequired(), Length(max=32)],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=32)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(max=32),
                                                     EqualTo("password_check", message="Passwords must match")],
                             render_kw={"placeholder": "Password"})
    password_check = PasswordField("Password", validators=[InputRequired(), Length(max=32)],
                                   render_kw={"placeholder": "Confirm password"})
    email = EmailField("Email", validators=[InputRequired(), Length(max=256), Email()],
                       render_kw={"placeholder": "Email"})
    submit = SubmitField("Sign In")
