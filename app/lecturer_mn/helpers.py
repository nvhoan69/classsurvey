fields = [
        'stt',
        'username',
        'password',
        'full_name',
        'vnu_email'
    ]

fields_len = 5

fields_render = [
        'Tên đăng nhập',
        'Họ và tên',
        'VNU email',
    ]

dicts_list = []

def excel_list_to_dict(excel_list):
    dicts_list.clear()
    i = 0
    for property in excel_list: #property: STT ,username, password, full_name, vnu_email
        dict = {}
        for j in range(fields_len):
            try:
                check = int(property[j])
                if str(property[j]).isdigit():
                    dict[fields[j]] = property[j]  # if property[j] is a integer
                else:
                    dict[fields[j]] = property[j].strip()  # for the student_code

            except ValueError:
                dict[fields[j]] = property[j].strip()

        dicts_list.append(dict)
        i += 1

    # print(dicts_list)

    return dicts_list