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
from flask import abort
from app.roles import Role


def set_field(new_value, old_value):
    if new_value:
        return new_value
    else:
        return old_value


def parse_filter(class_):
    params = list(request.args.keys())
    if len(params) and hasattr(class_, params[0]):
        field = params[0]
        data = request.args[field]
        results = class_.query.filter_by(**{field: data})  # 'class_' is database model
        return results
    else:
        return class_.query.all()


@application.route("/admin_panel")
@roles_required(Role.Admin)
def admin_panel():
    return render_template("admin/index.html")


@application.route("/admin_panel/students")
def admin_panel_students():
    return render_template("admin/students.html", students=parse_filter(models.Student))


@application.route("/admin_panel/students/new", methods=["GET", "POST"])
def admin_panel_students_new():
    new_form = forms.AdminRegistrationStudentForm()
    if new_form.validate_on_submit():
        user = models.User(new_form.authorization_code.data, new_form.name.data, new_form.surname.data, 
                           new_form.password.data, 0, new_form.email.data)
        db.session.add(user)
        db.session.commit()
        student = models.Student(user.id_)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('admin_panel_students'))
    return render_template("admin/students.html", students=parse_filter(models.Student), new_form=new_form)


@application.route("/admin_panel/students/<id_>", methods=["GET", "POST"])
def admin_panel_students_update(id_):
    update_form = forms.AdminUpdateStudentForm()
    current_student = models.Student.query.filter_by(id=id_).first()
    if update_form.validate_on_submit():
        current_student.student_user_data.name = set_field(update_form.name.data,
                                                           current_student.student_user_data.name)
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
    return render_template("admin/students.html", students=parse_filter(models.Student),
                           current_student=current_student, update_form=update_form)


@application.route("/admin_panel/parents")
def admin_panel_parents():
    return render_template("admin/parents.html", mothers=parse_filter(models.Mother),
                           fathers=parse_filter(models.Father))


@application.route("/admin_panel/parents/new", methods=["GET", "POST"])
def admin_panel_parents_new():
    new_form = forms.AdminRegistrationParentForm()
    if new_form.validate_on_submit():
        if new_form.type.data == "mother":
            user = models.User(new_form.authorization_code.data, new_form.name.data, new_form.surname.data,
                               new_form.password.data, 1, new_form.email.data)
            db.session.add(user)
            db.session.commit()
            mother = models.Mother(user.id_)
            db.session.add(mother)
            db.session.commit()
        elif new_form.type.data == "father":
            user = models.User(new_form.authorization_code.data, new_form.name.data, new_form.surname.data,
                               new_form.password.data, 2, new_form.email.data)
            db.session.add(user)
            db.session.commit()
            father = models.Father(user.id_)
            db.session.add(father)
            db.session.commit()
        return redirect(url_for('admin_panel_parents'))
    return render_template("admin/parents.html", mothers=models.Mother.query.all(), fathers=models.Father.query.all(),
                           new_form=new_form)


@application.route("/admin_panel/mothers/mothers/<id_>", methods=["GET", "POST"])
def admin_panel_mothers_update(id_):
    update_form = forms.AdminUpdateParentForm()
    current_mother = models.Mother.query.filter_by(id=id_).first()
    if update_form.validate_on_submit():
        current_mother.mother_user_data.name = set_field(update_form.name.data,
                                                         current_mother.mother_user_data.name)
        current_mother.mother_user_data.surname = set_field(update_form.surname.data,
                                                            current_mother.mother_user_data.surname)
        current_mother.mother_user_data.password = set_field(update_form.password.data,
                                                             current_mother.mother_user_data.password)
        current_mother.mother_user_data.email = set_field(update_form.email.data,
                                                          current_mother.mother_user_data.email)
        db.session.commit()
        return redirect(url_for('admin_panel_mothers'))
    return render_template("admin/mothers.html", mothers=models.Mother.query.all(), fathers=models.Father.query.all(),
                           current_mother=current_mother, update_form=update_form)


@application.route("/admin_panel/parents/fathers/<id_>", methods=["GET", "POST"])
def admin_panel_fathers_update(id_):
    update_form = forms.AdminUpdateParentForm()
    current_father = models.Father.query.filter_by(id=id_).first()
    if update_form.validate_on_submit():
        current_father.father_user_data.name = set_field(update_form.name.data,
                                                         current_father.father_user_data.name)
        current_father.father_user_data.surname = set_field(update_form.surname.data,
                                                            current_father.father_user_data.surname)
        current_father.father_user_data.password = set_field(update_form.password.data,
                                                             current_father.father_user_data.password)
        current_father.father_user_data.email = set_field(update_form.email.data,
                                                          current_father.father_user_data.email)
        db.session.commit()
        return redirect(url_for('admin_panel_fathers'))
    return render_template("admin/fathers.html", mothers=models.Mother.query.all(), fathers=models.Father.query.all(),
                           current_father=current_father, update_form=update_form)


@application.route("/admin_panel/teachers")
def admin_panel_teachers():
    return render_template("admin/parents.html", teachers=parse_filter(models.Teacher))


@application.route("/admin_panel/teachers/new", methods=["GET", "POST"])
def admin_panel_teachers_new():
    new_form = forms.AdminRegistrationForm()
    if new_form.validate_on_submit():
        user = models.User(new_form.authorization_code.data, new_form.name.data, new_form.surname.data,
                           new_form.password.data, 1, new_form.email.data)
        db.session.add(user)
        db.session.commit()
        teacher = models.Teacher(user.id_)
        db.session.add(teacher)
        return redirect(url_for('admin_panel_teachers'))
    return render_template("admin/teachers.html", teachers=models.Mother.query.all(), new_form=new_form)


@application.route("/admin_panel/teachers/<id_>", methods=["GET", "POST"])
def admin_panel_teachers_update(id_):
    update_form = forms.AdminUpdateForm()
    current_teacher = models.Teacher.query.filter_by(id=id_).first()
    if update_form.validate_on_submit():
        current_teacher.teacher_user_data.name = set_field(update_form.name.data,
                                                           current_teacher.teacher_user_data.name)
        current_teacher.teacher_user_data.surname = set_field(update_form.surname.data,
                                                              current_teacher.teacher_user_data.surname)
        current_teacher.teacher_user_data.password = set_field(update_form.password.data,
                                                               current_teacher.teacher_user_data.password)
        current_teacher.teacher_user_data.email = set_field(update_form.email.data,
                                                            current_teacher.teacher_user_data.email)
        db.session.commit()
        return redirect(url_for('admin_panel_teachers'))
    return render_template("admin/teachers.html", teachers=models.Teacher.query.all(), current_teacher=current_teacher,
                           update_form=update_form)


@application.route("/admin_panel/classes")
def admin_panel_classes():
    return render_template("admin/classes.html", classes=parse_filter(models.Class))


@application.route("/admin_panel/classes/new", methods=["GET", "POST"])
def admin_panel_classes_new():
    new_form = forms.AdminRegistrationClassForm()
    if new_form.validate_on_submit():
        class_ = models.Class(new_form.number, new_form.symbol, new_form.class_manager_id)
        db.session.add(class_)
        db.session.commit()
        return redirect(url_for('admin_panel_classes'))
    return render_template("admin/classes.html", classes=models.Class.query.all(), new_form=new_form)


@application.route("/admin_panel/classes/<id_>", methods=["GET", "POST"])
def admin_panel_classes_update(id_):
    update_form = forms.AdminUpdateClassForm()
    current_class = models.Class.query.filter_by(id=id_).first()
    if update_form.validate_on_submit():
        db.session.commit()
        return redirect(url_for('admin_panel_classes'))
    return render_template("admin/classes.html", classs=models.Class.query.all(), current_class=current_class,
                           update_form=update_form)


@application.route("/admin_panel/subjects")
def admin_panel_subjects():
    return render_template("admin/subjects.html", subjects=parse_filter(models.Subject))


@application.route("/admin_panel/subjects/new")
def admin_panel_subjects_new():
    new_form = forms.AdminRegistrationSubjectForm()
    if new_form.validate_on_submit():
        subject = models.Subject(new_form.name)
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('admin_panel_subjects'))
    return render_template("admin/subjects.html", subjects=models.Subject.query.all(), new_form=new_form)


@application.route("/admin_panel/subjects/<id_>")
def admin_panel_subjects_update(id_):
    update_form = forms.AdminUpdateStudentForm()
    current_subject = models.Subject.query.filter_by(id=id_).first()
    if update_form.validate_on_submit():
        db.session.commit()
        return redirect(url_for('admin_panel_subjects'))
    return render_template("admin/subjects.html", subjects=models.Subject.query.all(), current_subject=current_subject,
                           update_form=update_form)


@application.route("/admin_panel/lessons")
def admin_panel_lessons():
    return render_template("admin/lessons.html", lessons=parse_filter(models.Lesson))


@application.route("/admin_panel/lessons/new")
def admin_panel_lessons_new():
    new_form = forms.AdminRegistrationClassForm()
    if new_form.validate_on_submit():
        class_ = models.Class(new_form.number, new_form.symbol, new_form.class_manager_id)
        db.session.add(class_)
        db.session.commit()
        return redirect(url_for('admin_panel_lessons'))
    return render_template("admin/lessons.html", lessons=models.Lesson.query.all(), new_form=new_form)


@application.route("/admin_panel/lessons/<id_>")
def admin_panel_lessons_update(id_):
    update_form = forms.AdminUpdateLessonForm()
    current_lesson = models.Lesson.query.filter_by(id=id_).first()
    if update_form.validate_on_submit():
        db.session.commit()
        return redirect(url_for('admin_panel_lessons'))
    return render_template("admin/lessons.html", lessons=models.Lesson.query.all(), current_lesson=current_lesson,
                           update_form=update_form)


@application.route("/admin_panel/timetable")
def admin_panel_timetable():
    return render_template("admin/timetable.html", timetables=parse_filter(models.Timetable))


@application.route("/admin_panel/timetable/new")
def admin_panel_timetable_new():
    return "Page"


@application.route("/admin_panel/timetable/<id_>")
def admin_panel_timetable_update(id_):
    return "Page"


@application.route("/admin_panel/cabinets")
def admin_panel_cabinets():
    return render_template("admin/cabinets.html", cabinets=parse_filter(models.Cabinet))


@application.route("/admin_panel/cabinets/new")
def admin_panel_cabinets_new():
    new_form = forms.AdminRegistrationCabinetForm()
    if new_form.validate_on_submit():
        cabinet = models.Cabinet(new_form.number, new_form.name)
        db.session.add(cabinet)
        db.session.commit()
        return redirect(url_for('admin_panel_cabinets'))
    return render_template("admin/cabinets.html", cabinets=models.Cabinet, new_form=new_form)


@application.route("/admin_panel/cabinets/<id_>")
def admin_panel_cabinets_update(id_):
    update_form = forms.AdminUpdateCabinetForm()
    current_cabinet = models.Cabinet.query.filter_by(id=id_).first()
    if update_form.validate_on_submit():
        db.session.commit()
        return redirect(url_for('admin_panel_cabinets'))
    return render_template("admin/cabinets.html", cabinets=models.Cabinet.query.all(), current_cabinet=current_cabinet,
                           update_form=update_form)


@application.route("/admin_panel/rates")
def admin_panel_rates():
    return render_template("admin/rates.html", rates=parse_filter(models.Rate))


@application.route("/admin_panel/rates/new")
def admin_panel_rates_new():
    new_form = forms.AdminRegistrationRateForm()
    if new_form.validate_on_submit():
        rate = models.Rate(new_form.rate, new_form.student_id, new_form.lesson_id)
        db.session.add(rate)
        db.session.commit()
        return redirect(url_for('admin_panel_rates'))
    return render_template("admin/rates.html", rates=models.Rate.query.all(), new_form=new_form)


@application.route("/admin_panel/rates/<id_>")
def admin_panel_rates_update(id_):
    update_form = forms.AdminUpdateRateForm()
    current_rate = models.Rate.query.filter_by(id=id_).first()
    if update_form.validate_on_submit():
        db.session.commit()
        return redirect(url_for('admin_panel_rates'))
    return render_template("admin/rates.html", rates=models.Rate.query.all(), current_rate=current_rate,
                           update_form=update_form)


@application.route("/admin_panel/textbooks")
def admin_panel_textbooks():
    return render_template("admin/textbooks.html", textbooks=parse_filter(models.Textbook))


@application.route("/admin_panel/textbooks/new")
def admin_panel_textbooks_new():
    new_form = forms.AdminRegistrationTextbookForm()
    if new_form.validate_on_submit():
        textbook = models.Textbook(new_form.subject_id, new_form.class_number, new_form.link)
        db.session.add(textbook)
        db.session.commit()
        return redirect(url_for('admin_panel_textbooks'))
    return render_template("admin/textbooks.html", textbooks=models.Textbook.query.all(), new_form=new_form)


@application.route("/admin_panel/textbooks/<id_>")
def admin_panel_textbooks_update(id_):
    update_form = forms.AdminUpdateTextbookForm()
    current_textbook = models.Textbook.query.filter_by(id=id_).first()
    if update_form.validate_on_submit():
        db.session.commit()
        return redirect(url_for('admin_panel_textbooks'))
    return render_template("admin/textbooks.html", textbooks=models.Textbook.query.all(),
                           current_textbook=current_textbook, update_form=update_form)


@application.route("/admin_panel/achievements")
def admin_panel_achievements():
    return render_template("admin/achievements.html", achievements=parse_filter(models.Achievement))


@application.route("/admin_panel/achievements/new")
def admin_panel_achievements_new():
    new_form = forms.AdminRegistrationAchievementForm()
    if new_form.validate_on_submit():
        achievement = models.Achievement(new_form.name, new_form.text, new_form.score)
        db.session.add(achievement)
        db.session.commit()
        return redirect(url_for('admin_panel_achievement'))
    return render_template("admin/achievement.html", achievements=models.Lesson.query.all(), new_form=new_form)


@application.route("/admin_panel/achievements/<id_>")
def admin_panel_achievements_update(id_):
    update_form = forms.AdminUpdateAchievementForm()
    current_achievement = models.Achievement.query.filter_by(id=id_).first()
    if update_form.validate_on_submit():
        db.session.commit()
        return redirect(url_for('admin_panel_achievements'))
    return render_template("admin/achievements.html", acievements=models.Achievement.query.all(), 
                           current_acievement=current_achievement, update_form=update_form)
