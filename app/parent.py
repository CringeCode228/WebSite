from app import application
from flask import render_template
from flask_user import roles_required
from flask_login import current_user
from app.roles import Role
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
