from bcrypt import gensalt, hashpw
from flask_login import UserMixin
from marshmallow import fields

from sqlalchemy import Column, Boolean, DateTime, Float, ForeignKey, Index, LargeBinary, String, TIMESTAMP, Table, Text, text, \
    create_engine
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, MEDIUMTEXT, TINYINT
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from app import login_manager, ma

engine = create_engine('mysql+mysqlconnector://classsurvey:123@localhost:3306/ourdb', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
metadata = Base.metadata

class Role(Base):
    __tablename__ = 'role'

    id = Column(INTEGER(11), primary_key=True)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)

class User(Base, UserMixin):

    __tablename__ = 'user'
    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(16, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    password = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    role_id = Column(INTEGER(11), ForeignKey('role.id'))

    role = relationship("Role")

    def update(self, password, **kwargs):
        value = hashpw(password.encode('utf8'), gensalt())
        setattr(self, 'password', value)
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property in ('username'):
                setattr(self, property, value)

    def __init__(self, password,**kwargs):
        self.update(password, **kwargs)

    def __repr__(self):
        return str(self.username)

    def get_id(self):
        return self.id

    def allowed(self, access_level):
        return access_level == self.role.code

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None



class Student(Base):
    __tablename__ = 'student'

    id = Column(INTEGER(11), primary_key=True)
    student_code = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    # dob = Column(Date)
    full_name = Column(String(255, 'utf8mb4_unicode_ci'))
    vnu_email = Column(String(64, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    class_course = Column(String(45, 'utf8mb4_unicode_ci'))
    user_id = Column(ForeignKey('user.id'), nullable=False, unique=True)

    user = relationship('User', backref=backref("user_student"))

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property in ('student_code', 'full_name', 'vnu_email', 'class_course'):
                setattr(self, property, value)


class StudentSchema(ma.ModelSchema):
    class Meta:
        model = Student
        fields = ('id', 'student_code', 'full_name', 'vnu_email', 'class_course')

class Lecturer(Base):
    __tablename__ = 'lecturer'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    full_name = Column(String(255, 'utf8mb4_unicode_ci'))
    vnu_email = Column(String(64, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, unique=True)

    user = relationship('User', backref=backref("user_lecturer", uselist=False))

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property in ('username', 'full_name', 'vnu_email'):
                setattr(self, property, value)

class LecturerSchema(ma.ModelSchema):
    class Meta:
        model = Lecturer
        fields = ('id', 'username', 'full_name', 'vnu_email')


t_course_student = Table('course_student', Base.metadata,
    Column('course_id', INTEGER, ForeignKey('course.id')),
    Column('student_id', INTEGER, ForeignKey('student.id'))
)

class Course(Base):

    __tablename__ = 'course'

    id = Column(INTEGER(11), primary_key=True)
    course_code = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    name = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)

    lecturer_id = Column(INTEGER(11), ForeignKey('lecturer.id'), nullable=False)
    lecturer = relationship("Lecturer", backref=backref("lecturer_courses"))
    students = relationship("Student", secondary=t_course_student, backref=backref("student_courses"))

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property in ('course_code', 'name'):
                setattr(self, property, value)

class CourseSchema(ma.ModelSchema):
    lecturer = ma.Nested(LecturerSchema, only=['full_name'])

    class Meta:
        model = Course
        fields = ('id', 'course_code', 'name', 'lecturer')

t_survey_student = Table('survey_student', Base.metadata,
    Column('survey_id', INTEGER, ForeignKey('survey.id')),
    Column('student_id', INTEGER, ForeignKey('student.id'))
)

class Survey(Base):

    __tablename__ = 'survey'

    id = Column(INTEGER(11), primary_key=True)
    survey_title = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course_id = Column(INTEGER(11), ForeignKey('course.id'), nullable=False)

    course = relationship("Course", backref=backref("course_surveys"))
    students = relationship("Student", secondary=t_survey_student, backref=backref("student_surveys"))

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property in ('survey_title'):
                setattr(self, property, value)

class SurveySchema(ma.ModelSchema):
    course = ma.Nested(CourseSchema, only=['course_code', 'name', 'lecturer'])

    class Meta:
        model = Course
        fields = ('id', 'course', 'survey_title', 'created_at', 'modified_at')

class Version(Base):

    __tablename__ = 'version'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255, 'utf8mb4_unicode_ci'), unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_default = Column(Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property in ('name', 'is_default'):
                setattr(self, property, value)

class VersionSchema(ma.ModelSchema):
    class Meta:
        model = Version
        fields = ('id', 'created_at', 'modified_at', 'name', 'is_default')


class Tieuchi(Base):
    __tablename__ = 'tieuchi'

    id = Column(INTEGER(11), primary_key=True)
    stt = Column(INTEGER(11), nullable=False)
    content = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)

    danhmuc_id = Column(INTEGER(11), ForeignKey('danhmuc.id'), nullable=False)
    danhmuc = relationship("Danhmuc", backref=backref("tieuchis"))

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property in ('stt', 'content'):
                setattr(self, property, value)

class Danhmuc(Base):
    __tablename__ = 'danhmuc'

    id = Column(INTEGER(11), primary_key=True)
    stt = Column(INTEGER(11), nullable=False)
    content = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)

    version_id = Column(INTEGER(11), ForeignKey('version.id'), nullable=False)
    version = relationship("Version", backref=backref("danhmucs"))

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property in ('stt', 'content'):
                setattr(self, property, value)

class TieuchiSchema(ma.ModelSchema):
    class Meta:
        model = Tieuchi
        fields = ('stt', 'content')

class DanhmucSchema(ma.ModelSchema):
    tieuchis = ma.Nested(TieuchiSchema, many=True)

    class Meta:
        model = Danhmuc
        fields = ('stt', 'content', 'tieuchis')

class Points(Base):
    __tablename__ = 'points'

    id = Column(INTEGER(11), primary_key=True)
    tieuchi_id = Column(INTEGER(11), nullable=False)
    survey_id = Column(INTEGER(11), nullable=False)
    student_id = Column(INTEGER(11), nullable=False)
    points = Column(INTEGER(3), nullable=False)

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property in ('points', 'tieuchi_id', 'survey_id', 'student_id'):
                setattr(self, property, value)

class Result(Base):
    __tablename__ = 'result'

    id = Column(INTEGER(11), primary_key=True)
    tieuchi_id = Column(INTEGER(11), nullable=False)
    survey_id = Column(INTEGER(11), nullable=False)
    tb = Column(Float, nullable=False)

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property in ('tb', 'tieuchi_id', 'survey_id'):
                setattr(self, property, value)

class Commit(Base):
    __tablename__ = 'commit'

    id = Column(INTEGER(11), primary_key=True)
    student_id = Column(INTEGER(11), nullable=False)
    version_id = Column(INTEGER(11), nullable=False)
    survey_id = Column(INTEGER(11), nullable=False)
    is_commited = Column(Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property in ('is_commited', 'student_id', 'version_id', 'survey_id'):
                setattr(self, property, value)

metadata.create_all(engine)