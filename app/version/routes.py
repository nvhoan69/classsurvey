import json

from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from app.version import blueprint
from app.base.helpers import requires_access_level, version_factory, version_reset_default, version_set_default as set_default
from app.base.models import Version, VersionSchema, db_session
from app.base.forms import EditVersion

fields = ['name', 'created_at', 'modified_at', 'is_default']
fields_render = ['Tên mẫu', 'Tạo lúc', 'Lần sửa cuối', 'Mặc định']

@blueprint.route('/index')
@login_required
@requires_access_level('admin')
def version_index():
    versions = Version.query.all()
    schema = VersionSchema(many=True)
    output = schema.dump(versions).data
    version_json = json.dumps(output)

    return render_template(
        '/version_management.html',
        fields=fields,
        fields_render=fields_render,
        propertis=version_json,
        form=EditVersion(request.form)
    )

@blueprint.route('/get/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def get_version(id):
    version = Version.query.filter_by(id=id).first()
    if not version:
        return "The version doesn't exist!"
    schema = VersionSchema()
    output = schema.dump(version).data

    return jsonify(output)

@blueprint.route('/process', methods=['POST'])
@login_required
@requires_access_level('admin')
def process_version():
    data = request.form.to_dict()
    code, version = version_factory(**data)
    if 1 == code:
        return render_template('errors/page_404.html')
    schema = VersionSchema()
    output = schema.dump(version).data

    return jsonify(output)

@blueprint.route('/delete/<id>', methods=['POST'])
@login_required
@requires_access_level('admin')
def delete_version(id):
    version = Version.query.filter_by(id=id).first()
    if not version:
        return render_template('errors/page_404.html')

    is_default = version.is_default
    db_session.delete(version)
    db_session.commit()

    if is_default:
        version_reset_default()
    return jsonify('Success')

@blueprint.route('/set_default/<id>')
@login_required
@requires_access_level('admin')
def version_set_default(id):
    set_default(id)
    versions = Version.query.all()
    schema = VersionSchema(many=True)
    output = schema.dump(versions).data
    version_json = json.dumps(output)

    return render_template(
        '/version_management.html',
        fields=fields,
        fields_render=fields_render,
        propertis=version_json,
        form=EditVersion(request.form)
    )