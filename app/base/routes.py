from bcrypt import checkpw
from flask import render_template, redirect, request, url_for, session
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app.base import blueprint
from app.base.forms import LoginForm
from app.base.models import User, Student, Role, Course, Lecturer
from app.base.models import db_session


@blueprint.route('/')
def route_default():
    # create role table.
    if not Role.query.filter_by(code='admin').first():
        role = Role(code='admin', name='admin')
        db_session.add(role)
        db_session.commit()
    if not Role.query.filter_by(code='student').first():
        role = Role(code='student', name='sinh vien')
        db_session.add(role)
        db_session.commit()
    if not Role.query.filter_by(code='lecturer').first():
        role = Role(code='lecturer', name='giang vien')
        db_session.add(role)
        db_session.commit()

    # create default admin
    if not User.query.filter_by(username='Admin').first():
        user = User(username='Admin', password='123')
        admin_role = Role.query.filter_by(code='admin').first()
        user.role = admin_role
        db_session.add(user)
        db_session.commit()

    # for test
    if not Course.query.filter_by(course_code='INT3306 1').first():
        course = Course(course_code='INT3306 1', name='Phát triển ứng dụng Web')

        lecturer = Lecturer.query.filter_by(username='thanhld').first()
        course.lecturer = lecturer
        course.students.append(Student.query.first())

        db_session.add(course)
        db_session.commit()

    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

## Login


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and checkpw(password.encode('utf8'), bytes(user.password, 'utf8')):
            login_user(user)

            if user.allowed('admin'):
                session['level_access'] = 'admin'
                return redirect(url_for('admin_blueprint.index'))

            if user.allowed('student'):
                session['level_access'] = 'student'
                return redirect(url_for('student_blueprint.index'))

            if user.allowed('lecturer'):
                session['level_access'] = 'lecturer'
                return redirect(url_for('lecturer_blueprint.index'))

        return render_template('errors/page_403.html')

    if not current_user.is_authenticated or not session.get('level_access'):
        return render_template(
            'login/login.html',
            login_form=login_form,
        )
    return redirect(url_for('{}_blueprint.index'.format(session.get('level_access'))))

@blueprint.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('base_blueprint.login'))

