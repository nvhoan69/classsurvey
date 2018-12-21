fields = [
        'stt',
        'student_code',
        'password',
        'full_name',
        'vnu_email',
        'khoa'
    ]

fields_len = 6

fields_render = [
        'MSV/Tài khoản',
        'Họ và tên',
        'VNU email',
        'Khóa đào tạo'
    ]

dicts_list = []

def excel_list_to_dict(excel_list):
    dicts_list.clear()
    i = 0
    for property in excel_list: #property: STT ,code, password, full_name, vnu_email, khoa
        dict = {}
        for j in range(fields_len):
            for j in range(fields_len):
                try:
                    check = int(property[j])
                    if str(property[j]).isdigit():
                        dict[fields[j]] = property[j] #if property[j] is a integer
                    else:
                        dict[fields[j]] = property[j].strip() #for the student_code

                except ValueError:
                    dict[fields[j]] = property[j].strip()

        dicts_list.append(dict)
        i += 1

    # print(dicts_list)

    return dicts_list