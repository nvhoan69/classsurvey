import math

from app.base.models import Result, Points, Survey, Course

def compute(a, b, c, d, e):
    if a + b + c + d + e == 0:# tránh gây lỗi
        return 0, 0
    m = (a + 2 * b + 3 * c + 4 * d + 5 * e) / (a + b + c + d + e)
    std = (1 - m) ** 2 + (2 - m) ** 2 + (3 - m) ** 2 + (4 - m) ** 2 + (5 - m) ** 2
    std = (std / 4) ** (0.5)

    return round(m, 2), round(std, 2)

def computeFromPoints(points):# tính M, STD từ danh sách các points
    a = b = c = d = e = 0
    for po in points:
        if po.points == 1:
            a +=1
        if po.points == 2:
            b +=1
        if po.points == 3:
            c +=1
        if po.points == 4:
            d +=1
        if po.points == 5:
            e +=1
    m, std = computeMSTD(a, b, c, d, e)
    return m, std

def computeMSTD(survey_id, tieuchi_id):# tính M, STD cho môn học của giảng viên
    points = Points.query.filter_by(survey_id=survey_id, tieuchi_id=tieuchi_id).all()# lấy ra danh sách các points đánh giá của 1 giảng viên
    m, std = computeFromPoints(points)
    return m, std

def computeMSTD1(survey_id, tieuchi_id):# tính M, STD cho môn học của các giảng viên khác dạy cùng môn
    # lấy ra danh sách các lớp của các giảng viên khác dạy cùng môn
    survey = Survey.query.filter_by(survey_id=survey_id).first()
    course = survey.course
    name = course.name
    courses = Course.query.filter_by(name=name).all()
    courses.remove(course)

    #lấy ra danh sách các points để dùng hàm computeFromPoints()
    points = []
    for co in courses:
        survey = co.course_surveys[0]
        if survey:
            for po in Points.query.filter_by(survey_id=survey.id, tieuchi_id=tieuchi_id).all():
                points.append(po)

    m, std = computeFromPoints(points)
    return m, std

def computeMSTD2(survey_id, tieuchi_id): # tính M, STD cho tất cả các lớp giảng viên dạy
    survey = Survey.query.filter_by(survey_id=survey_id).first()
    course = survey.course
    lecturer = course.lecturer
    courses = lecturer.lecturer_courses # lấy danh sách các lớp do giảng viên đó dạy

    # lấy ra danh sách các points để dùng hàm computeFromPoints()
    points = []
    for co in courses:
        survey = co.course_surveys[0]
        if survey:
            for po in Points.query.filter_by(survey_id=survey.id, tieuchi_id=tieuchi_id).all():
                points.append(po)

    m, std = computeFromPoints(points)
    return m, std