import json
import pandas as pd
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from app.survey import blueprint
from app.base.helpers import requires_access_level, student_factory, course_factory
from app.base.models import Survey, SurveySchema, db_session, Lecturer, StudentSchema, Student, Course, CourseSchema
from app.base.forms import EditSurvey, AddStudent

from app.survey.helpers import excel_list_to_dict, retrieve_info

fields = ['title', 'created_at', 'modified_at']
fields_render = ['Tiêu đề', 'Tạo lúc', 'Lần sửa cuối']

@blueprint.route('/index')
@login_required
@requires_access_level('admin')
def survey_index():
    surveys = Survey.query.all()
    schema = SurveySchema(many=True)
    output = schema.dump(surveys).data

    # print(output)
    survey_json = json.dumps(output)
    return render_template(
        '/survey_management.html',
        fields=fields,
        fields_render=fields_render,
        propertis=survey_json,
        form=EditSurvey(request.form)
    )

@blueprint.route('/course/index')
@login_required
@requires_access_level('admin')
def survey_course_index():
    fields = ['course_code', 'name', 'lecturer']
    fields_render = ['Mã môn học', 'Tên môn học', 'Giảng viên']
    courses = Course.query.all()
    course_schema = CourseSchema(many=True)
    output = course_schema.dump(courses).data

    # print(output)
    course_json = json.dumps(output)
    return render_template(
        '/survey_course_index.html',
        fields=fields,
        fields_render=fields_render,
        propertis=course_json
    )

@blueprint.route('/course/gen_survey/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def course_gen_survey(id):
    course = Course.query.filter_by(id=id).first()
    if not course:
        return "The course with that course's id doesn't exist!"
    title = course.name + ' ' + course.course_code

    survey = Survey.query.filter_by(title=title).first()
    if survey:
        # return jsonify('The survey has already existed!')
        return jsonify('Cuộc khảo sát này đã được tạo từ trước!')

    survey = Survey(title=title)
    survey.course = course
    for student in course.students:
        survey.students.append(student)

    db_session.add(survey)
    db_session.commit()

    return jsonify('Success')

@blueprint.route('/course/gen_survey_for_all', methods=['POST'])
@login_required
@requires_access_level('admin')
def course_gen_survey_for_all():
    courses = Course.query.all()
    count = 0
    for course in courses:
        title = course.name + ' ' + course.course_code
        survey = Survey.query.filter_by(title=title).first()
        if not survey:
            survey = Survey(title=title)
            survey.course = course
            for student in course.students:
                survey.students.append(student)

            db_session.add(survey)
            count += 1

    db_session.commit()

    return jsonify('Đã tạo thêm ' + str(count) + ' cuộc khảo sát.')

@blueprint.route('/get/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def get_survey(id):
    survey = Survey.query.filter_by(id=id).first()
    if not survey:
        return "The survey which has that id doesn't exist!"
    schema = SurveySchema()
    output = schema.dump(survey).data

    return jsonify(output)

# @blueprint.route('/process', methods=['POST'])
# @login_required
# @requires_access_level('admin')
# def process_lecturer():
#     data = request.form.to_dict()
#     course = course_factory(**data)
#     schema = CourseSchema()
#     output = schema.dump(course).data
#
#     return jsonify(output)

@blueprint.route('/delete/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def delete_survey(id):
    survey = Survey.query.filter_by(id=id).first()
    if not survey:
        return "The course with that course's id doesn't exist!"
    survey.students.clear()

    db_session.delete(survey)
    db_session.commit()
    return jsonify('Success')



# @blueprint.route('/student/process/<id>', methods=['POST'])
# @login_required
# @requires_access_level('admin')
# def course_student_process(id):
#     a = id
#     student_data = request.form.to_dict()
#     student = student_factory(**student_data)
#     course = Course.query.filter_by(id=id).first()
#     if not course: return "The course which has that id doesn't exist!"
#     if student not in course.students:
#         course.students.append(student)
#         db_session.commit()
#
#     student_schema = StudentSchema()
#     output = student_schema.dump(student).data
#
#     return jsonify(output)