from bcrypt import checkpw
from flask import render_template, redirect, request, url_for, session
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app.base import blueprint
from app.base.forms import LoginForm
from app.base.models import User, Role, Survey, Course, Version, Danhmuc, Tieuchi
from app.base.models import db_session

from app.base.helpers import version_factory

d = [
    'Cơ sở vật chất',
    'Môn học',
    'Hoạt động giảng dạy'
]

t = [
    'Giảng đường đáp ứng nhu cầu môn học',
    'Các trang thiết bị đáp ứng yêu cầu giảng dạy và học tập',
    'Bạn được hỗ trợ kịp thời trong quá trình học môn này',
    'Mục tiêu môn học nêu rõ kiến thức và kĩ năng của người học cần đạt',
    'Thời lượng môn học được phân bổ hợp lí cho các hình thức học tập',

    'Các tài liệu môn học được cập nhật',
    'Môn học góp phần trang bị kiến thức và kĩ năng nghề nghiệp cho bạn',
    'Giảng viên thực hiện đầy đủ nội dung và thời lượng của môn học theo kế hoạch',
    'Giảng viên hướng dẫn bạn phương pháp học tập khi bắt đầu bộ môn',
    'Phương pháp giảng dạy của giảng viên giúp bạn phát triển tư duy',

    'Giảng viên tạo cơ hội để bạn chủ động tham gia vào quá trình học tập',
    'Giảng viên giúp bạn phát triển kĩ năng làm việc độc lập',
    'Giảng viên giúp bạn rèn luyện phương pháp giữa các vấn đề liên hệ trong môn học thực tiễn',
    'Giảng viên sử dụng hiệu quả phương tiện dạy học',
    'Giảng viên quan tâm giáo dục tư cách, phẩm chất nghề nghiệp của người học',

    'Bạn hiểu được những vấn đề truyền tải trên lớp',
    'Kết quả học tập của người học được đánh giá bằng nhiều hình thức phù hợp với tính chất và đặc thù môn học',
    'Nội dung kiểm tra đánh giá tổng hợp được các kĩ năng mà người học phải đạt yêu cầu',
    'Thông tin phản hồi tử kiểm tra đánh giá giúp bạn cải thiện kết quả học tập',
]

@blueprint.route('/')
def route_default():
    # create role table.
    if not Role.query.filter_by(code='admin').first():
        role = Role(code='admin', name='admin')
        db_session.add(role)
        db_session.commit()
    if not Role.query.filter_by(code='student').first():
        role = Role(code='student', name='sinh vien')
        db_session.add(role)
        db_session.commit()
    if not Role.query.filter_by(code='lecturer').first():
        role = Role(code='lecturer', name='giang vien')
        db_session.add(role)
        db_session.commit()

    # create default admin
    if not User.query.filter_by(username='Admin').first():
        user = User(username='Admin', password='123')
        admin_role = Role.query.filter_by(code='admin').first()
        user.role = admin_role
        db_session.add(user)
        db_session.commit()

    #for test
    if not Version.query.filter_by(name='Version 1').first():
        code, version = version_factory(name='Version 1', is_default=False)
        db_session.add(version)
        db_session.commit()

    if not Version.query.filter_by(name='Version 2').first():
        code, version = version_factory(name='Version 2', is_default=False)
        db_session.add(version)
        db_session.commit()

    if not Version.query.filter_by(name='Version 3').first():
        code, version = version_factory(name='Version 3', is_default=False)
        db_session.add(version)
        db_session.commit()

    version = Version.query.filter_by(name='Version 1').first()
    if not Danhmuc.query.filter_by(version_id=version.id, content=d[0]).first():
        danhmuc = Danhmuc(stt=1, content=d[0])
        danhmuc.version = version
        db_session.add(danhmuc)

        tieuchi1 = Tieuchi(stt=1, content=t[0])
        tieuchi1.danhmuc = danhmuc
        tieuchi2 = Tieuchi(stt=2, content=t[1])
        tieuchi2.danhmuc = danhmuc

        db_session.add(tieuchi1)
        db_session.add(tieuchi2)
        db_session.commit()

    if not Danhmuc.query.filter_by(version_id=version.id, content=d[1]).first():
        danhmuc = Danhmuc(stt=2, content=d[1])
        danhmuc.version = version
        db_session.add(danhmuc)

        for i in range(3, 8):
            tieuchi = Tieuchi(stt=i, content=t[i-1])
            tieuchi.danhmuc = danhmuc
            db_session.add(tieuchi)
        db_session.commit()

    if not Danhmuc.query.filter_by(version_id=version.id, content=d[2]).first():
        danhmuc = Danhmuc(stt=3, content=d[2])
        danhmuc.version = version
        db_session.add(danhmuc)

        for i in range(8, 20):
            tieuchi = Tieuchi(stt=i, content=t[i-1])
            tieuchi.danhmuc = danhmuc
            db_session.add(tieuchi)
        db_session.commit()

        db_session.commit()

    version = Version.query.filter_by(name='Version 2').first()
    if not Danhmuc.query.filter_by(version_id=version.id, content=d[1]).first():
        danhmuc = Danhmuc(stt=1, content=d[1])
        danhmuc.version = version
        db_session.add(danhmuc)

        for i in range(3, 8):
            tieuchi = Tieuchi(stt=i - 2, content=t[i-1])
            tieuchi.danhmuc = danhmuc
            db_session.add(tieuchi)
        db_session.commit()

    version = Version.query.filter_by(name='Version 3').first()
    if not Danhmuc.query.filter_by(version_id=version.id, content=d[2]).first():
        danhmuc = Danhmuc(stt=1, content=d[2])
        danhmuc.version = version
        db_session.add(danhmuc)

        for i in range(8, 20):
            tieuchi = Tieuchi(stt=i - 7, content=t[i-1])
            tieuchi.danhmuc = danhmuc
            db_session.add(tieuchi)
        db_session.commit()

        db_session.commit()



    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

## Login


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and checkpw(password.encode('utf8'), bytes(user.password, 'utf8')):
            login_user(user)
            session['user_id'] = user.id

            if user.allowed('admin'):
                session['level_access'] = 'admin'
                return redirect(url_for('admin_blueprint.index'))

            if user.allowed('student'):
                session['level_access'] = 'student'
                return redirect(url_for('student_blueprint.index'))

            if user.allowed('lecturer'):
                session['level_access'] = 'lecturer'
                return redirect(url_for('lecturer_blueprint.index'))

        return render_template('errors/page_403.html')

    if not current_user.is_authenticated or not session.get('level_access'):
        return render_template(
            'login/login.html',
            login_form=login_form,
        )
    return redirect(url_for('{}_blueprint.index'.format(session.get('level_access'))))

@blueprint.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('base_blueprint.login'))

