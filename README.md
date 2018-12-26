# Khảo sát môn học

### Danh sách nhóm
| Sinh viên | MSSV |
| ------ | ------ |
| Nguyễn Văn Hoàn |  |
| Nguyễn Minh Châu | 15021766 |
| Nguyễn Trọng Đạt |  |

### Cài đặt các yêu cầu (requirements)
Chúng ta cần dùng pip để cài đặt một số các yêu cầu

```sh
$ pip install -r requirements.txt
```

### Khởi tạo cơ sở dữ liệu

```sh
$ CREATE DATABASE IF NOT EXISTS ourdb;
$ CREATE USER IF NOT EXISTS 'classsurvey'@'localhost' IDENTIFIED BY '123';
$ GRANT ALL PRIVILEGES ON mydb.* TO 'classsurvey'@'localhost';
```

### Demo
Khởi tạo server
```sh
$ python classsurvey.py
```

Mở web localhost (cổng 5000)
```sh
http://localhost:5000/
```

