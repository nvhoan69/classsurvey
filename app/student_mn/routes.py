import json

from app.student_mn import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required

from app.base.helpers import requires_access_level, student_factory
from app.base.models import Student, StudentSchema
from app.base.forms import AddStudent

from app import db

@blueprint.route('/index')
@login_required
@requires_access_level('admin')
def student_index():
    fields = [
        'student_code',
        'full_name',
        'vnu_email',
        'khoa'
    ]
    fields_render = [
        'MSV/Tài khoản',
        'Họ và tên',
        'VNU email',
        'Khóa đào tạo'
    ]

    students = Student.query.all()
    student_schema = StudentSchema(many=True)
    output = student_schema.dump(students).data
    students_json = json.dumps(output)

    return render_template(
        '/student_management.html',
        fields=fields,
        fields_render = fields_render,
        students = students_json,
        form=AddStudent(request.form)
    )

@blueprint.route('/get/<student_id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def student_get(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        return render_template('errors/page_404.html')
    student_schema = StudentSchema()
    output = student_schema.dump(student).data

    return jsonify(output)


@blueprint.route('/process', methods=['POST'])
@login_required
@requires_access_level('admin')
def student_process():
    student_data = request.form.to_dict()
    student = student_factory(**student_data)
    student_schema = StudentSchema()
    output = student_schema.dump(student).data

    return jsonify(output)

@blueprint.route('/delete/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def student_delete(id):
    student = Student.query.filter_by(student_id=id).first()
    if not student:
        return render_template('errors/page_404.html')
    student.student_code = str(student.student_code) + '-Deleted' # not test yet, consider to add "-Deleted" to the account instead of delete directly
    db.session.commit()
    return jsonify('Success')