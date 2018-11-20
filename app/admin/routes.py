from app.admin import blueprint
from flask import render_template
from flask_login import login_required

from app.base.helpers import requires_access_level
from app.base.models import User


@blueprint.route('/')
@login_required
@requires_access_level('admin')
def index():
    return render_template('index.html')


@blueprint.route('/<template_1>/<template_2>')
@login_required
@requires_access_level('admin')
def route_template(template_1, template_2):
    if template_1 == 'student':
        users = User.query.filter_by(role=2).all()
        fields = [
            'username'
        ]

    if template_1 == 'lecturer':
        users = User.query.filter_by(role=1).all()
        fields = [
            'username'
        ]
    return render_template(template_1 + '/' + template_2 + '.html', fields=fields, users=users)