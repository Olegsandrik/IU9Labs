use master
GO

IF (
	SELECT name
	FROM sys.databases
	WHERE name = N'lab_7_Nikitin'
) IS NOT NULL
DROP DATABASE lab_7_Nikitin
GO

CREATE DATABASE lab_7_Nikitin
GO

use lab_7_Nikitin
GO

--- —оздать представление на основе одной из таблиц
--- задани€ 6

CREATE TABLE Pacient (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
	SNILS NVARCHAR(11) NOT NULL,
	Email NVARCHAR(255) NOT NULL,
);
GO

CREATE VIEW my_first_view AS
	SELECT ID, Name, SNILS
	FROM Pacient;
GO

INSERT INTO Pacient(Name, SNILS, Email) VALUES ('Alex', '12345678900', 'Alex@mail.ru');
INSERT INTO Pacient(Name, SNILS, Email) VALUES ('Igor', '12345678900', 'Igor@mail.ru');
INSERT INTO Pacient(Name, SNILS, Email) VALUES ('Vova', '12345678901', 'Vova@mail.ru');
INSERT INTO Pacient(Name, SNILS, Email) VALUES ('Ignat', '12345678904', 'Ignat@mail.ru');
GO

SELECT * FROM my_first_view; -- ѕредставление работы представлени€ (оно динамически мен€етс€ в зависимости от данных в таблице, тк не проиндексировано)
GO

DROP VIEW my_first_view
GO

--- —оздать представление на основе полей обеих
--- св€занных таблиц задани€ 6

CREATE TABLE Doctor (
    DoctorID INT PRIMARY KEY,
    PassportNum NVARCHAR(10),
	Name NVARCHAR(50),
	Surname NVARCHAR(50),
	Middlename NVARCHAR(50),
	Specialization NVARCHAR(30),
);

CREATE TABLE Diploma (
    diplomID INT PRIMARY KEY,
    RegistrNum INT NOT NULL,
	Name NVARCHAR(20) NOT NULL,
	Surname NVARCHAR(20) NOT NULL,
	Middlename NVARCHAR(20),
	DiplomDate DATE NOT NULL,
	AcademicDegree NVARCHAR(20) NOT NULL,
    DoctorID INT,
    CONSTRAINT FK_Child_Parent FOREIGN KEY (DoctorID)
        REFERENCES Doctor(DoctorID)
        ON DELETE CASCADE
);
GO

CREATE VIEW Doctor_with_diploma_view 
WITH SCHEMABINDING AS
	SELECT doc.DoctorID, doc.PassportNum, doc.Name, doc.Surname, 
       dip.diplomID, dip.RegistrNum, dip.DiplomDate, dip.AcademicDegree
	FROM dbo.Doctor AS doc 
	INNER JOIN dbo.Diploma AS dip ON doc.DoctorID = dip.DoctorID;
GO

INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, MiddleName, Specialization) VALUES (1, '4518737303', 'Alex', 'Nikitin', 'Vladimirovich', 'Pediatr');
INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, MiddleName, Specialization) VALUES (2, '4518737304', 'Valera', 'Kotov', 'Vladimirovich', 'Pediatr');
INSERT INTO Diploma (diplomID, RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree, DoctorID) VALUES (1, '356736', 'Alex', 'Nikitin', 'Vladimirovich', '15.7.2008', 'bacalavr', 1);
INSERT INTO Diploma (diplomID, RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree, DoctorID) VALUES (2, '356736', 'Alex', 'Nikitin', 'Vladimirovich', '15.7.2024', 'magistr', 1);
GO

SELECT * FROM Doctor_with_diploma_view;
GO


DROP VIEW Doctor_with_diploma_view
DROP TABLE Diploma, Doctor
GO

--- —оздать индекс дл€ одной из таблиц задани€ 6,
--- включив в него дополнительные неключевые пол€.

CREATE INDEX PacientIndex
	ON Pacient (Name) 
	INCLUDE (SNILS, Email) -- добавит в индекс, но не будут €вл€тьс€ частью ключа индекса
GO

SELECT Email FROM Pacient WHERE Name = 'Alex' and SNILS = '12345678900';
GO

--DROP INDEX PacientIndex on Pacient;
GO

--- —оздать индексированное представление.

CREATE VIEW pacient_index_view
WITH SCHEMABINDING AS
	SELECT pac.Name, pac.SNILS, pac.Email
	FROM dbo.Pacient as pac
	WHERE pac.Name LIKE '%a%';
GO

CREATE UNIQUE CLUSTERED INDEX pacient_email_index
	ON pacient_index_view (email)
GO

SELECT Email FROM pacient_index_view;
SELECT Email FROM Pacient;
GO

--DROP VIEW pacient_index_view;
--DROP TABLE Pacient;
GO