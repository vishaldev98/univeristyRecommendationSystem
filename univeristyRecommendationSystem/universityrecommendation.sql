
create database universityrecommendation;
use universityrecommendation;

CREATE TABLE StudentInfo (
    studentId INT AUTO_INCREMENT PRIMARY KEY,
    StudentName VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(15),
    IELTS DECIMAL(3, 1),
    Transcript VARCHAR(255),
    Percentage DECIMAL(5, 2),
    address VARCHAR(255),
    country VARCHAR(100),
    city VARCHAR(100)
);

CREATE TABLE University (
    universityId INT AUTO_INCREMENT PRIMARY KEY,
    universityName VARCHAR(100) NOT NULL,
    universityLocation VARCHAR(255)
);

