from functools import wraps
from flask import url_for, redirect, session, render_template
from app.base.models import User, Student, Role, Lecturer, Course, Survey, Version, db_session

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('level_access'):
                return redirect(url_for('base_blueprint.login'))

            if not access_level == session.get('level_access'):
                return render_template('errors/page_403.html')
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def requires_access_user(user_id):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('user_id'):
                return redirect(url_for('base_blueprint.login'))

            if not user_id == session.get('user_id'):
                return render_template('errors/page_403.html')
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def student_factory(**kwargs):
    value = ''
    if 'id' in kwargs.keys():
        value = kwargs['id']

    if value:
        student = Student.query.filter_by(id=value).first()
        if student:
            student.update(**kwargs)
    else:
        check1 = Student.query.filter_by(student_code=kwargs['student_code']).first()
        check2 = Student.query.filter_by(vnu_email=kwargs['vnu_email']).first()

        if check1:
            return check1
        if check2:
            return check2

        role = Role.query.filter_by(code='student').first()
        user = User(password=kwargs['student_code'], username=kwargs['student_code'])
        user.role = role

        student = Student(
            student_code = kwargs['student_code'],
            full_name = kwargs['full_name'],
            vnu_email=kwargs['vnu_email'],
            class_course=kwargs['class_course'],
        )
        student.user = user

        db_session.add(user)
        db_session.add(student)

    db_session.commit()
    return student

def lecturer_factory(**kwargs):
    value = ''
    if 'id' in kwargs.keys():
        value = kwargs['id']

    if value:
        lecturer = Lecturer.query.filter_by(id=value).first()
        if lecturer:
            lecturer.update(**kwargs)
    else:
        check1 = Lecturer.query.filter_by(username=kwargs['username']).first()
        check2 = Lecturer.query.filter_by(vnu_email=kwargs['vnu_email']).first()
        if check1:
            return check1
        if check2:
            return check2

        role = Role.query.filter_by(code='lecturer').first()
        user = User(password=kwargs['username'], username=kwargs['username'])
        user.role = role

        lecturer = Lecturer(
            username = kwargs['username'],
            full_name = kwargs['full_name'],
            vnu_email=kwargs['vnu_email'],
        )
        lecturer.user = user

        db_session.add(user)
        db_session.add(lecturer)
    db_session.commit()
    return lecturer

def course_factory(**kwargs):
    value = ''
    if 'id' in kwargs.keys():
        value = kwargs['id']

    if value:
        course = Course.query.filter_by(id=value).first()
        if not course:
            return "The course doesn't exist!"

        course.update(**kwargs)
    db_session.commit()
    return course


def survey_factory(**kwargs):
    value = ''
    if 'id' in kwargs.keys():
        value = kwargs['id']

    if value:
        survey = Survey.query.filter_by(id=value).first()
        if not survey:
            return "The course doesn't exist!"

        survey.update(**kwargs)
    db_session.commit()
    return survey

def version_factory(**kwargs):
    value = ''
    if 'id' in kwargs.keys():
        value = kwargs['id']

    if value:
        version = Version.query.filter_by(id=value).first()
        if not version:
            return 1, "The version doesn't exist!"
        if 'name' in kwargs.keys():
            name = kwargs['name']
            version2 = Version.query.filter_by(name=name).first()
            if version2:
                if version2.id == version.id:
                    return 1, 'The version is not be change'
                else:
                    return 1, 'The name is already used!'

        version.update(**kwargs)

    else:
        if 'name' in kwargs.keys():
            name = kwargs['name']
            check = Version.query.filter_by(name=name).first()
            if not check:
                version = Version(**kwargs)
                db_session.add(version)
            version_default = Version.query.filter_by(is_default=True).first()
            if not version_default:
                version.update(is_default=True)

    db_session.commit()
    return 0, version

def version_reset_default():
    versions = Version.query.all()
    for ver in versions:
        ver.update(is_default=False)

    version = Version.query.first()
    if version:
        version.update(is_default=True)

    db_session.commit()

def version_set_default(id):
    version = Version.query.filter_by(id=id).first()
    if version:
        versions = Version.query.all()
        for ver in versions:
            ver.update(is_default=False)
        version.update(is_default=True)

    db_session.commit()



