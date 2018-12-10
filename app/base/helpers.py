from functools import wraps
from flask import url_for, redirect, session, render_template
from app import db
from app.base.models import User, ACCESS, Student, Lecturer

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

def student_factory(**kwargs):
    value = kwargs['student_id']
    if value:
        student = Student.query.filter_by(student_id=value).first()
        if student:
            student.update(**kwargs)
    else:
        student = Student(
            student_code = kwargs['student_code'],
            full_name = kwargs['full_name'],
            vnu_email=kwargs['vnu_email'],
            khoa=kwargs['khoa'],
            user_id=3
        )
        db.session.add(student)
    db.session.commit()
    return student

def lecturer_factory(**kwargs):
    value = kwargs['lecturer_id']
    if value:
        lecturer = Lecturer.query.filter_by(lecturer_id=value).first()
        if lecturer:
            lecturer.update(**kwargs)
    else:
        lecturer = Lecturer(
            account = kwargs['account'],
            full_name = kwargs['full_name'],
            vnu_email=kwargs['vnu_email'],
            user_id=3
        )
        db.session.add(lecturer)
    db.session.commit()
    return lecturer



