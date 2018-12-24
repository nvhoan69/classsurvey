fields = [
        'stt',
        'student_code',
        'full_name',
        'dob',
        'class_course',
        'note',
        'vnu_email'
    ]

fields_len = 6

fields_render = [
        'MSV/Tài khoản',
        'Họ và tên',
        'VNU email',
        'Khóa đào tạo'
    ]

filted_list = []
dicts_list = []

def excel_list_to_dict(excel_list):
    filted_list.clear()
    for a in excel_list:
        try:
            check = int(a[0])
            filted_list.append(a)
        except ValueError:
            pass

    dicts_list.clear()
    i = 0
    for property in filted_list: #property: STT ,student_code, full_name, dob, class_course, note
        dict = {}
        for j in range(fields_len):
            for j in range(fields_len):
                try:
                    property[j] = str(property[j])
                    check = int(property[j])
                    if str(property[j]).isdigit():
                        if int(property[j]) > 1000:# if property[j] is student_code
                            property[j] = str(property[j])
                        dict[fields[j]] = property[j] #if property[j] is a integer
                    else:
                        dict[fields[j]] = property[j].strip() #for the student_code
                        print("Hello")

                except ValueError:
                    dict[fields[j]] = property[j].strip()
        dict['vnu_email'] = str(dict['student_code']) + '@vnu.edu.vn'

        dicts_list.append(dict)
        i += 1

    # for a in dicts_list:
    #     print(a)

    return dicts_list

def retrieve_info(excel_list):
    filted_list.clear()

    for a in excel_list:
        try:
            check = int(a[0])
            break
        except ValueError:
            filted_list.append(a)

    # for a in filted_list:
    #     print(a)

    dict = {}
    dict['lecturer'] = filted_list[5][2].strip()
    dict['lecturer_code'] = str(filted_list[5][4]).strip()
    dict['lecturer_username'] = filted_list[5][5].strip()
    dict['semester'] = filted_list[3][0].strip()
    dict['course_code'] = filted_list[7][2].strip()
    dict['course_name'] = filted_list[8][2].strip()

    # print(dict)

    return dict