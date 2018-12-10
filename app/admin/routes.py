import json

from app.admin import blueprint
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from app.base.helpers import requires_access_level, student_factory, lecturer_factory
from app.base.models import Student, StudentSchema, Lecturer, LecturerSchema, Course
from app.base.forms import AddStudent, AddLecturer

from app.admin.dtos import studentDTO
from app import db


@blueprint.route('/')
@login_required
@requires_access_level('admin')
def index():
    return render_template('index.html')


# @blueprint.route('/student/student_management')
# @login_required
# @requires_access_level('admin')
# def students_list():
#     fields = [
#         'student_code',
#         'full_name',
#         'vnu_email',
#         'khoa'
#     ]
#     fields_render = [
#         'MSV/Tài khoản',
#         'Họ và tên',
#         'VNU email',
#         'Khóa đào tạo'
#     ]
#
#     students = Student.query.all()
#     student_schema = StudentSchema(many=True)
#     output = student_schema.dump(students).data
#     students_json = json.dumps(output)
#
#     return render_template(
#         '/student/student_management.html',
#         fields=fields,
#         fields_render = fields_render,
#         students = students_json,
#         form=AddStudent(request.form)
#     )
#
# @blueprint.route('/student/get/<student_id>', methods=['POST'])
# @login_required
# @requires_access_level('admin')
# def get_student(student_id):
#     student = Student.query.filter_by(student_id=student_id).first()
#     if not student:
#         return render_template('errors/page_404.html')
#     student_schema = StudentSchema()
#     output = student_schema.dump(student).data
#
#     return jsonify(output)
#
#
# @blueprint.route('/student/process_student', methods=['POST'])
# @login_required
# @requires_access_level('admin')
# def process_student():
#     student_data = request.form.to_dict()
#     student = student_factory(**student_data)
#     student_schema = StudentSchema()
#     output = student_schema.dump(student).data
#
#     return jsonify(output)
#
# @blueprint.route('/student/delete/<id>', methods=['POST'])
# @login_required
# @requires_access_level('admin')
# def delete_student(id):
#     student = Student.query.filter_by(student_id=id).first()
#     if not student:
#         return render_template('errors/page_404.html')
#     student.student_code = str(student.student_code) + '-Deleted';  # not test yet, consider to use active instead of delete directly
#     db.session.commit()
#     return jsonify('Success')

# @blueprint.route('/lecturer/lecturer_management')
# @login_required
# @requires_access_level('admin')
# def lecturers_list():
#     fields = [
#         'account',
#         'full_name',
#         'vnu_email'
#     ]
#     fields_render = [
#         'Tên đăng nhập',
#         'Họ và tên',
#         'VNU email',
#     ]
#
#     lecturers = Lecturer.query.all()
#     lecturer_schema = LecturerSchema(many=True)
#     output = lecturer_schema.dump(lecturers).data
#     lecturer_json = json.dumps(output)
#
#     return render_template(
#         '/lecturer/lecturer_management.html',
#         fields=fields,
#         fields_render=fields_render,
#         lecturers=lecturer_json,
#         form=AddLecturer(request.form)
#     )
#
# @blueprint.route('/lecturer/get/<id>', methods=['POST'])
# @login_required
# @requires_access_level('admin')
# def get_lecturer(id):
#     lecturer = Lecturer.query.filter_by(lecturer_id=id).first()
#     if not lecturer:
#         return render_template('errors/page_404.html')
#     lecturer_schema = LecturerSchema()
#     output = lecturer_schema.dump(lecturer).data
#
#     return jsonify(output)
#
# @blueprint.route('/lecturer/process_lecturer', methods=['POST'])
# @login_required
# @requires_access_level('admin')
# def process_lecturer():
#     data = request.form.to_dict()
#     lecturer = lecturer_factory(**data)
#     lecturer_schema = LecturerSchema()
#     output = lecturer_schema.dump(lecturer).data
#
#     return jsonify(output)
#
# @blueprint.route('/lecturer/delete/<id>', methods=['POST'])
# @login_required
# @requires_access_level('admin')
# def delete_lecturer(id):
#     lecturer = Lecturer.query.filter_by(lecturer_id=id).first()
#     if not lecturer:
#         return render_template('errors/page_404.html')
#     lecturer.account = str(lecturer.account) + '-Deleted';  # not test yet, consider to use active instead of delete directly
#     db.session.commit()
#     return jsonify('Success')