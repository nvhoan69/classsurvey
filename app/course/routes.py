import json
import pandas as pd

from app.course import blueprint
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from app.base.helpers import requires_access_level, student_factory, course_factory
from app.base.models import Course, CourseSchema, db_session, Lecturer, StudentSchema, Student
from app.base.forms import EditCourse, AddStudent

from app.course.helpers import excel_list_to_dict, retrieve_info

fields = ['course_code', 'name', 'lecturer']
fields_render = ['Mã môn học', 'Tên môn học', 'Giảng viên', 'Sinh viên']

@blueprint.route('/index')
@login_required
@requires_access_level('admin')
def course_index():
    courses = Course.query.all()
    course_schema = CourseSchema(many=True)
    output = course_schema.dump(courses).data

    # print(output)
    course_json = json.dumps(output)
    return render_template(
        '/course_management.html',
        fields=fields,
        fields_render=fields_render,
        propertis=course_json,
        form=EditCourse(request.form)
    )

@blueprint.route('/get/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def get_course(id):
    course = Course.query.filter_by(id=id).first()
    if not course:
        return render_template('errors/page_404.html')
    course_schema = CourseSchema()
    output = course_schema.dump(course).data

    return jsonify(output)

@blueprint.route('/process', methods=['POST'])
@login_required
@requires_access_level('admin')
def process_lecturer():
    data = request.form.to_dict()
    course = course_factory(**data)
    schema = CourseSchema()
    output = schema.dump(course).data

    return jsonify(output)

@blueprint.route('/delete/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def delete_course(id):
    course = Course.query.filter_by(id=id).first()
    if not course:
        return "The course with that course's id doesn't exist!"
    course.students.clear()

    db_session.delete(course)
    db_session.commit()
    return jsonify('Success')

@blueprint.route('/excel_upload', methods=['POST', 'GET'])
@login_required
@requires_access_level('admin')
def course_excel_upload():
    if request.method == 'POST':
        print(request.files['file'])
        f = request.files['file']
        data_xls = pd.read_excel(f)#read excel file
        data_xls.fillna("nan", inplace=True)

        list = data_xls.values.tolist()
        dicts_list = excel_list_to_dict(list)# list of student dict
        info_dict = retrieve_info(list) # retrieve course's name, code, lecturer

        course = Course.query.filter_by(course_code=info_dict['course_code']).first()
        if not course:
            course = Course(course_code=info_dict['course_code'], name=info_dict['course_name'])
            lecturer = Lecturer.query.filter_by(username=info_dict['lecturer_username']).first()
            if not lecturer: return "the lecturer with the lecturer's username doesn't exist!"
            course.lecturer = lecturer

        for data in dicts_list:# create student in database and add each to the course
            student = student_factory(**data)
            course.students.append(student)

        db_session.commit()

        return redirect(url_for('course_blueprint.course_student_index', id=course.id))
    return render_template('upload.html')

@blueprint.route('/student/index/<id>')
@login_required
@requires_access_level('admin')
def course_student_index(id):
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

    course = Course.query.filter_by(id=id).first()
    if not course: return "The course with that id doesn't exist!"
    students = course.students
    student_schema = StudentSchema(many=True)
    output = student_schema.dump(students).data
    students_json = json.dumps(output)

    course_schema = CourseSchema()
    output = course_schema.dump(course).data
    course_json = json.dumps(output)

    return render_template(
        'course_student_management.html',
        course = course_json,
        fields=fields,
        fields_render=fields_render,
        students=students_json,
        form=AddStudent(request.form)
    )

@blueprint.route('/student/process/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def course_student_process(id):
    a = id
    student_data = request.form.to_dict()
    student = student_factory(**student_data)
    course = Course.query.filter_by(id=id).first()
    if not course: return "The course which has that id doesn't exist!"
    if student not in course.students:
        course.students.append(student)
        db_session.commit()

    student_schema = StudentSchema()
    output = student_schema.dump(student).data

    return jsonify(output)

@blueprint.route('/student/delete/<course_id>/<student_id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def course_student_delete(course_id, student_id):
    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return "The student who has the id doesn't exist!"
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return "The course which has the id doesn't exist!"
    course.students.remove(student)

    db_session.commit()
    return jsonify('Success')