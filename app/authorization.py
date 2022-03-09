from app import application
from app import loginManager
from app import models
from flask import render_template, flash, redirect, url_for
from app import forms
from flask_login import current_user, login_user, logout_user
from app import models
from app import db
from werkzeug.security import generate_password_hash
import random
from flask_login import login_required
from app import no_cache


@application.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template("/authorization/login.html", user=current_user, form=form, unic_id=random.random())


@application.route("/registration")
def registration():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User(form.username, form.password, form.email, models.Role.default)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("/authorization/registration.html", form=form)


@application.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@application.route("/profile")
@login_required
def profile():
    return render_template("/authorization/profile.html", user=current_user)


@loginManager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
