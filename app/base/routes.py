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
from app.base.models import User, ACCESS
from app import db


@blueprint.route('/')
def route_default():
    # create default users
    if not User.query.filter_by(username='Admin').first():
        user = User(username='Admin', password='123', role=ACCESS['admin'])
        db.session.add(user)
        db.session.commit()

    if not User.query.filter_by(username='Student').first():
        user = User(username='Student', password='123', role=ACCESS['student'])
        db.session.add(user)
        db.session.commit()

    if not User.query.filter_by(username='Lecturer').first():
        user = User(username='Lecturer', password='123', role=ACCESS['lecturer'])
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('base_blueprint.login'))


# @blueprint.route('/<template>')
# @login_required
# def route_template(template):
#     return render_template(template + '.html')
#


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

    if not current_user.is_authenticated:
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



