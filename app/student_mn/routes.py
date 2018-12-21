import json
import pandas as pd

from app.student_mn import blueprint
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from app.base.helpers import requires_access_level, student_factory
from app.base.models import Student, StudentSchema
from app.base.forms import AddStudent

from app.base.models import db_session

from app.student_mn.helpers import excel_list_to_dict

@blueprint.route('/index')
@login_required
@requires_access_level('admin')
def student_index():
    fields = [
        'student_code',
        'full_name',
        'vnu_email',
        'class_course'
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

@blueprint.route('/get/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def student_get(id):
    student = Student.query.filter_by(id=id).first()
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
    student = Student.query.filter_by(id=id).first()
    if not student:
        return render_template('errors/page_404.html')
    user = student.user
    # student.student_code = str(student.student_code) + '-Deleted' # not test yet, consider to add "-Deleted" to the account instead of delete directly
    db_session.delete(user)
    db_session.delete(student)

    db_session.commit()
    return jsonify('Success')

@blueprint.route('/excel_upload', methods=['POST', 'GET'])
@login_required
@requires_access_level('admin')
def lecturer_excel_upload():
    if request.method == 'POST':
        print(request.files['file'])
        f = request.files['file']
        data_xls = pd.read_excel(f)#read excel file
        # STT ,code, password, full_name, vnu_email, khoa

        dicts_list = excel_list_to_dict(data_xls.values.tolist())# list of student_dict
        for data in dicts_list:# create student in database
            student_factory(**data)

        return redirect(url_for('student_mn_blueprint.student_index'))
    return render_template('upload.html')