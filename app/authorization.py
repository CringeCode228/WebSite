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
from app import db
from flask_user.user_manager import UserManager
from flask import abort
import random, string


@application.route("/login", methods=["GET", "POST"])
def login():

    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(id_=form.id_.data).first()
        if user is None:
            flash('User not found')
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            flash('Invalid password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        print(current_user)
        return redirect(url_for('index'))
    return render_template("/authorization/login.html", user=current_user, form=form)


@application.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@loginManager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


class MyUserManager(UserManager):
    def unauthenticated_view(self):
        return abort(404)


userManager = MyUserManager(application, db, models.User)
