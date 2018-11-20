from app.student import blueprint
from flask import render_template
from flask_login import login_required

from app.base.helpers import requires_access_level


@blueprint.route('/')
@login_required
@requires_access_level('student')
def index():
    return render_template('student.html')