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
from app.base.models import User, Role, Survey, Course, Version, Danhmuc, Tieuchi
from app.base.models import db_session

from app.base.helpers import version_factory


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

    #for test
    if not Version.query.filter_by(name='Version 1').first():
        code, version = version_factory(name='Version 1', is_default=False)
        db_session.add(version)
        db_session.commit()

    if not Version.query.filter_by(name='Version 2').first():
        code, version = version_factory(name='Version 2', is_default=False)
        db_session.add(version)
        db_session.commit()

    if not Version.query.filter_by(name='Version 3').first():
        code, version = version_factory(name='Version 3', is_default=False)
        db_session.add(version)
        db_session.commit()

    version = Version.query.filter_by(name='Version 1').first()
    if not Danhmuc.query.filter_by(version_id=version.id, content='Danh muc 1 v1').first():
        danhmuc = Danhmuc(stt=1, content='Danh muc 1 v1')
        danhmuc.version = version
        db_session.add(danhmuc)

        tieuchi1 = Tieuchi(stt=1, content='Tieu chi 1 v1')
        tieuchi1.danhmuc = danhmuc
        tieuchi2 = Tieuchi(stt=2, content='Tieu chi 2 v1')
        tieuchi2.danhmuc = danhmuc
        tieuchi3 = Tieuchi(stt=3, content='Tieu chi 3 v1')
        tieuchi3.danhmuc = danhmuc

        db_session.add(tieuchi1)
        db_session.add(tieuchi2)
        db_session.add(tieuchi3)
        db_session.commit()

    if not Danhmuc.query.filter_by(version_id=version.id, content='Danh muc 2 v1').first():
        danhmuc = Danhmuc(stt=2, content='Danh muc 2 v1')
        danhmuc.version = version
        db_session.add(danhmuc)

        tieuchi4 = Tieuchi(stt=4, content='Tieu chi 4 v1')
        tieuchi4.danhmuc = danhmuc
        tieuchi5 = Tieuchi(stt=5, content='Tieu chi 5 v1')
        tieuchi5.danhmuc = danhmuc

        db_session.add(tieuchi4)
        db_session.add(tieuchi5)


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
            session['user_id'] = user.id

            if user.allowed('admin'):
                session['level_access'] = 'admin'
                return redirect(url_for('admin_blueprint.index'))

            if user.allowed('student'):
                session['level_access'] = 'student'
                return redirect(url_for('student_blueprint.student_survey_index'))

            if user.allowed('lecturer'):
                session['level_access'] = 'lecturer'
                return redirect(url_for('lecturer_blueprint.student_survey_index'))

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

