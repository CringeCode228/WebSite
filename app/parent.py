from app import application
from app import loginManager
from flask import render_template, redirect, url_for
from app import forms
from flask_login import current_user, login_user, logout_user
from app import models
from app import db
from werkzeug.security import generate_password_hash
from flask_login import login_required
from flask import request
from flask_user import roles_required
from flask_login import current_user
from flask import abort, send_from_directory
from app.roles import Role
from werkzeug.utils import secure_filename
from app.config import UPLOAD_FOLDER
import os
from flask import flash
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import Mother, Father


def get_self():
    if current_user.type == 1:
        return Mother.query.filter_by(user_id=current_user.id_).first()
    else:
        return Father.query.filter_by(user_id=current_user.id_).first()


@application.route("/parents/me/profile")
@roles_required(Role.Parent)
def parent_profile():
    parent = get_self()
    if current_user.type == 1:
        return render_template("parents/profile.html", mother=parent)
    else:
        return render_template("parents/profile.html", father=parent)
