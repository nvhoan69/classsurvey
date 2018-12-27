import json
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from app.result import blueprint
from app.base.helpers import requires_access_level, survey_factory
from app.base.models import Survey, SurveySchema, db_session, Course, CourseSchema

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
        '/result_survey_management.html',
        fields=fields,
        fields_render=fields_render,
        propertis=survey_json
    )