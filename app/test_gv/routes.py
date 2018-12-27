import json

from app.test_gv import blueprint
from flask import render_template, session
from flask_login import login_required

from app.base.helpers import requires_access_level
from app.base.models import Course, Survey, User, Version, SurveySchema, Danhmuc, DanhmucSchema

fields = ['survey_title', 'created_at', 'modified_at']
fields_render = ['Tiêu đề', 'Tạo lúc', 'Lần sửa cuối']

@blueprint.route('/')
@blueprint.route('/index')
@login_required
@requires_access_level('lecturer')
def index():
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    lecturer = user.user_lecturer

    courses = lecturer.lecturer_courses
    surveys = []

    for co in courses:
        sur = co.course_surveys[0]
        if sur:
            surveys.append(sur)

    schema = SurveySchema(many=True)
    output = schema.dump(surveys).data

    # print(output)
    survey_json = json.dumps(output)
    return render_template(
        '/lecturer_survey_management.html',
        fields=fields,
        fields_render=fields_render,
        propertis=survey_json
    )
