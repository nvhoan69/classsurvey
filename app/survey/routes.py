import json
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from app.survey import blueprint
from app.base.helpers import requires_access_level, survey_factory
from app.base.models import Survey, SurveySchema, db_session, Course, CourseSchema
from app.base.forms import EditSurvey

fields = ['survey_title', 'created_at', 'modified_at']
fields_render = ['Tiêu đề', 'Tạo lúc', 'Lần sửa cuối']

@blueprint.route('/index')
@login_required
@requires_access_level('admin')
def survey_index():
    surveys = Survey.query.all() # query tất cả các cuộc khảo sát

    schema = SurveySchema(many=True)
    output = schema.dump(surveys).data
    survey_json = json.dumps(output) # chuyển dứ liệu về json để trả về
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

    survey = Survey.query.filter_by(survey_title=title).first()
    if survey:
        # return jsonify('The survey has already existed!')
        return jsonify('Cuộc khảo sát này đã được tạo từ trước!')

    survey = Survey(survey_title=title)
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
        survey = Survey.query.filter_by(survey_title=title).first()
        if not survey:
            survey = Survey(survey_title=title)
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

@blueprint.route('/process', methods=['POST'])
@login_required
@requires_access_level('admin')
def process_lecturer():
    data = request.form.to_dict()
    survey = survey_factory(**data)
    schema = SurveySchema()
    output = schema.dump(survey).data

    return jsonify(output)

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
