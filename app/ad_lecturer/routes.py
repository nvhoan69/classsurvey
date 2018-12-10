import json

from app.ad_lecturer import blueprint
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from app.base.helpers import requires_access_level, lecturer_factory
from app.base.models import Lecturer, LecturerSchema
from app.base.forms import AddLecturer

from app import db

@blueprint.route('/lecturer/lecturer_management')
@login_required
@requires_access_level('admin')
def lecturers_list():
    fields = [
        'account',
        'full_name',
        'vnu_email'
    ]
    fields_render = [
        'Tên đăng nhập',
        'Họ và tên',
        'VNU email',
    ]

    lecturers = Lecturer.query.all()
    lecturer_schema = LecturerSchema(many=True)
    output = lecturer_schema.dump(lecturers).data
    lecturer_json = json.dumps(output)

    return render_template(
        '/lecturer/lecturer_management.html',
        fields=fields,
        fields_render=fields_render,
        lecturers=lecturer_json,
        form=AddLecturer(request.form)
    )

@blueprint.route('/lecturer/get/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def get_lecturer(id):
    lecturer = Lecturer.query.filter_by(lecturer_id=id).first()
    if not lecturer:
        return render_template('errors/page_404.html')
    lecturer_schema = LecturerSchema()
    output = lecturer_schema.dump(lecturer).data

    return jsonify(output)

@blueprint.route('/lecturer/process_lecturer', methods=['POST'])
@login_required
@requires_access_level('admin')
def process_lecturer():
    data = request.form.to_dict()
    lecturer = lecturer_factory(**data)
    lecturer_schema = LecturerSchema()
    output = lecturer_schema.dump(lecturer).data

    return jsonify(output)

@blueprint.route('/lecturer/delete/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def delete_lecturer(id):
    lecturer = Lecturer.query.filter_by(lecturer_id=id).first()
    if not lecturer:
        return render_template('errors/page_404.html')
    lecturer.account = str(lecturer.account) + '-Deleted';  # not test yet, consider to use active instead of delete directly
    db.session.commit()
    return jsonify('Success')