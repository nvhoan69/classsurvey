CREATE DATABASE IF NOT EXISTS ourdb;
CREATE USER IF NOT EXISTS 'classsurvey'@'localhost' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON mydb.* TO 'classsurvey'@'localhost';
