import json

from app.test_sv import blueprint
from flask import render_template, session
from flask_login import login_required

from app.base.helpers import requires_access_level
from app.base.models import Course, Survey, User, Version, SurveySchema, Danhmuc, DanhmucSchema

fields = ['survey_title', 'created_at', 'modified_at']
fields_render = ['Tiêu đề', 'Tạo lúc', 'Lần sửa cuối']

@blueprint.route('/')
@blueprint.route('/index')
@login_required
@requires_access_level('student')
def student_survey_index():
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    student = user.user_student[0]
    surveys = student.student_surveys
    schema = SurveySchema(many=True)
    output = schema.dump(surveys).data

    # print(output)
    survey_json = json.dumps(output)
    return render_template(
        '/student_survey_management.html',
        fields=fields,
        fields_render=fields_render,
        propertis=survey_json
    )

@blueprint.route('/assess/<id>')
@login_required
@requires_access_level('student')
def student_assess(id):
    version = Version.query.filter_by(is_default=True).first()
    danhmucs = version.danhmucs
    schema = DanhmucSchema(many=True)
    output = schema.dump(danhmucs).data

    danhmuc_json = json.dumps(output)
    return render_template('/student.html', danhmucs=danhmuc_json)

