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
from flask import request

from app.models import Student
import app.models


def set_field(new_value, old_value):
    if new_value:
        return new_value
    else:
        return old_value


@application.route("/admin_panel")
def admin_panel():
    current_student = Student.query.filter_by(id=id).first()
    return render_template("admin/index.html")


@application.route("/admin_panel/students")
def admin_panel_students():
    return render_template("admin/students.html", students=Student.query.all())


@application.route("/admin_panel/students/new", methods=["GET", "POST"])
def admin_panel_students_new():
    new_form = forms.AdminRegistrationStudentForm()
    if new_form.validate_on_submit():
        user = models.User(new_form.authorization_code.data, new_form.name.data, new_form.surname.data, new_form.password.data, 0,
                           new_form.email.data)
        db.session.add(user)
        db.session.commit()
        student = models.Student(user.id)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('admin_panel_students'))
    return render_template("admin/students.html", students=Student.query.all(), new_form=new_form)


@application.route("/admin_panel/students/<int:id>", methods=["GET", "POST"])
def admin_panel_students_update(id):
    update_form = forms.AdminUpdateStudentForm()
    current_student = Student.query.filter_by(id=id).first()
    if update_form.validate_on_submit():
        current_student.student_user_data.name = set_field(update_form.name.data, current_student.student_user_data.name)
        current_student.student_user_data.surname = set_field(update_form.surname.data,
                                                              current_student.student_user_data.surname)
        current_student.student_user_data.password = set_field(update_form.password.data,
                                                               current_student.student_user_data.password)
        current_student.student_user_data.email = set_field(update_form.email.data,
                                                            current_student.student_user_data.email)
        current_student.student_class_data = set_field(update_form.class_id.data, current_student.student_class_data)
        current_student.mother = set_field(update_form.mother_id.data, current_student.mother)
        current_student.father = set_field(update_form.father_id.data, current_student.father)
        current_student.score = set_field(update_form.score.data, current_student.score)
        db.session.commit()
        return redirect(url_for('admin_panel_students'))
    return render_template("admin/students.html", students=Student.query.all(), current_student=current_student,
                           update_form=update_form)


@application.route("/admin_panel/parents")
def admin_panel_parents():
    return render_template("admin/parents.html", mothers=models.Mother.query.all(), fathers=models.Father.query.all())


@application.route("/admin_panel/parents/new", methods=["GET", "POST"])
def admin_panel_parents_new():
    new_form = forms.AdminRegistrationParentForm()
    if new_form.validate_on_submit():
        if new_form.type.data == "mother":
            user = models.User(new_form.authorization_code.data, new_form.name.data, new_form.surname.data,
                               new_form.password.data, 1, new_form.email.data)
            db.session.add(user)
            db.session.commit()
            mother = models.Mother(user.id)
            db.session.add(mother)
            db.session.commit()
        elif new_form.type.data == "father":
            user = models.User(new_form.authorization_code.data, new_form.name.data, new_form.surname.data,
                               new_form.password.data, 2, new_form.email.data)
            db.session.add(user)
            db.session.commit()
            father = models.Father(user.id)
            db.session.add(father)
            db.session.commit()
        return redirect(url_for('admin_panel_parents'))
    return render_template("admin/parents.html", mothers=models.Mother.query.all(), fathers=models.Father.query.all(),
                           new_form=new_form)


@application.route("/admin_panel/parents/<id>", methods=["GET", "POST"])
def admin_panel_parents_update(id):
    return "Page"


@application.route("/admin_panel/teachers")
def admin_panel_teachers():
    return render_template("admin/parents.html", teachers=models.Teacher.query.all())


@application.route("/admin_panel/teachers/new", methods=["GET", "POST"])
def admin_panel_teachers_new():
    new_form = forms.AdminRegistrationForm()
    if new_form.validate_on_submit():
        user = models.User(new_form.authorization_code.data, new_form.name.data, new_form.surname.data,
                           new_form.password.data, 1, new_form.email.data)
        db.session.add(user)
        db.session.commit()
        teacher = models.Teacher(user.id)
        db.session.add(teacher)
        return redirect(url_for('admin_panel_teachers'))
    return render_template("admin/teachers.html", teachers=models.Mother.query.all(), new_form=new_form)


@application.route("/admin_panel/teachers/<id>", methods=["GET", "POST"])
def admin_panel_teachers_update(id):
    return "Page"


@application.route("/admin_panel/classes")
def admin_panel_classes():
    return render_template("admin/classes.html", classes=models.Class.query.all())


@application.route("/admin_panel/classes/new", methods=["GET", "POST"])
def admin_panel_classes_new():
    new_form = forms.AdminRegistrationClassForm()
    if new_form.validate_on_submit():
        class_ = models.Class(new_form.number, new_form.symbol, new_form.class_manager_id)
        db.session.add(class_)
        db.session.commit()
        return redirect(url_for('admin_panel_classes'))
    return render_template("admin/classes.html", students=models.Class.query.all(), new_form=new_form)


@application.route("/admin_panel/classes/<id>", methods=["GET", "POST"])
def admin_panel_classes_update(id):
    return "Page"


@application.route("/admin_panel/subjects")
def admin_panel_subjects():
    return render_template("admin/subjects.html", classes=models.Subject.query.all())


@application.route("/admin_panel/subjects/new")
def admin_panel_subjects_new():
    new_form = forms.AdminRegistrationSubjectForm()
    if new_form.validate_on_submit():
        subject = models.Subject(new_form.name)
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('admin_panel_subjects'))
    return render_template("admin/subjects.html", students=models.Subject.query.all(), new_form=new_form)


@application.route("/admin_panel/subjects/<id>")
def admin_panel_subjects_update(id):
    return "Page"


@application.route("/admin_panel/lessons")
def admin_panel_lessons():
    return render_template("admin/lessons.html", classes=models.Lesson.query.all())


@application.route("/admin_panel/lessons/new")
def admin_panel_lessons_new():
    new_form = forms.AdminRegistrationClassForm()
    if new_form.validate_on_submit():
        class_ = models.Class(new_form.number, new_form.symbol, new_form.class_manager_id)
        db.session.add(class_)
        db.session.commit()
        return redirect(url_for('admin_panel_lessons'))
    return render_template("admin/lessons.html", students=models.Lesson.query.all(), new_form=new_form)


@application.route("/admin_panel/lessons/<id>")
def admin_panel_lessons_update(id):
    return "Page"


@application.route("/admin_panel/timetable")
def admin_panel_timetable():
    return render_template("admin/timetable.html", classes=models.Timetable.query.all())


@application.route("/admin_panel/timetable/new")
def admin_panel_timetable_new():
    return "Page"


@application.route("/admin_panel/timetable/<id>")
def admin_panel_timetable_update(id):
    return "Page"


@application.route("/admin_panel/cabinets")
def admin_panel_cabinets():
    return render_template("admin/cabinets.html", classes=models.Cabinet.query.all())


@application.route("/admin_panel/cabinets/new")
def admin_panel_cabinets_new():
    new_form = forms.AdminRegistrationCabinetForm()
    if new_form.validate_on_submit():
        cabinet = models.Cabinet(new_form.number, new_form.name)
        db.session.add(cabinet)
        db.session.commit()
        return redirect(url_for('admin_panel_cabinets'))
    return render_template("admin/cabinets.html", students=models.Cabinet.query.all(), new_form=new_form)


@application.route("/admin_panel/cabinets/<id>")
def admin_panel_cabinets_update(id):
    return "Page"


@application.route("/admin_panel/rates")
def admin_panel_rates():
    return render_template("admin/rates.html", classes=models.Rate.query.all())


@application.route("/admin_panel/rates/new")
def admin_panel_rates_new():
    new_form = forms.AdminRegistrationRateForm()
    if new_form.validate_on_submit():
        rate = models.Rate(new_form.rate, new_form.student_id, new_form.lesson_id)
        db.session.add(rate)
        db.session.commit()
        return redirect(url_for('admin_panel_rates'))
    return render_template("admin/rates.html", students=models.Rate.query.all(), new_form=new_form)


@application.route("/admin_panel/rates/<id>")
def admin_panel_rates_update(id):
    return "Page"


@application.route("/admin_panel/textbooks")
def admin_panel_textbooks():
    return render_template("admin/textbooks.html", classes=models.Textbook.query.all())


@application.route("/admin_panel/textbooks/new")
def admin_panel_textbooks_new():
    new_form = forms.AdminRegistrationTextbookForm()
    if new_form.validate_on_submit():
        textbook = models.Textbook(new_form.subject_id, new_form.class_number, new_form.link)
        db.session.add(textbook)
        db.session.commit()
        return redirect(url_for('admin_panel_textbooks'))
    return render_template("admin/textbooks.html", students=models.Textbook.query.all(), new_form=new_form)


@application.route("/admin_panel/textbooks/<id>")
def admin_panel_textbooks_update(id):
    return "Page"


@application.route("/admin_panel/achievements")
def admin_panel_achievements():
    return render_template("admin/achievements.html", classes=models.Achievement.query.all())


@application.route("/admin_panel/achievements/new")
def admin_panel_achievements_new():
    new_form = forms.AdminRegistrationAchievementForm()
    if new_form.validate_on_submit():
        achievement = models.Achievement(new_form.name, new_form.text, new_form.score)
        db.session.add(achievement)
        db.session.commit()
        return redirect(url_for('admin_panel_achievement'))
    return render_template("admin/achievement.html", students=models.Lesson.query.all(), new_form=new_form)


@application.route("/admin_panel/achievements/<id>")
def admin_panel_achievements_update(id):
    return "Page"
