import json
import pandas as pd

from app.lecturer_mn import blueprint
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from app.base.helpers import requires_access_level, lecturer_factory
from app.base.models import Lecturer, LecturerSchema, db_session
from app.base.forms import AddLecturer

from app.lecturer_mn.helpers import excel_list_to_dict

fields = [
        'username',
        'full_name',
        'vnu_email'
    ]
fields_render = [
        'Tên đăng nhập',
        'Họ và tên',
        'VNU email',
    ]

@blueprint.route('/index')
@login_required
@requires_access_level('admin')
def lecturer_index():
    lecturers = Lecturer.query.all()
    lecturer_schema = LecturerSchema(many=True)
    output = lecturer_schema.dump(lecturers).data
    lecturer_json = json.dumps(output)

    return render_template(
        '/lecturer_management.html',
        fields=fields,
        fields_render=fields_render,
        lecturers=lecturer_json,
        form=AddLecturer(request.form)
    )

@blueprint.route('/get/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def get_lecturer(id):
    lecturer = Lecturer.query.filter_by(id=id).first()
    if not lecturer:
        return render_template('errors/page_404.html')
    lecturer_schema = LecturerSchema()
    output = lecturer_schema.dump(lecturer).data

    return jsonify(output)

@blueprint.route('/process', methods=['POST'])
@login_required
@requires_access_level('admin')
def process_lecturer():
    data = request.form.to_dict()
    lecturer = lecturer_factory(**data)
    lecturer_schema = LecturerSchema()
    output = lecturer_schema.dump(lecturer).data

    return jsonify(output)

@blueprint.route('/delete/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def delete_lecturer(id):
    lecturer = Lecturer.query.filter_by(id=id).first()
    if not lecturer:
        return render_template('errors/page_404.html')
    # lecturer.account = str(lecturer.account) + '-Deleted'  # not test yet, consider to add "-Deleted" to the account instead of delete directly
    user = lecturer.user

    db_session.delete(user)
    db_session.delete(lecturer)
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
        # STT ,username, password, full_name, vnu_email

        dicts_list = excel_list_to_dict(data_xls.values.tolist())# list of lecturer_dict
        for data in dicts_list:# create lecturer in database
            lecturer_factory(**data)

        return redirect(url_for('lecturer_mn_blueprint.lecturer_index'))
    return render_template('upload.html')
