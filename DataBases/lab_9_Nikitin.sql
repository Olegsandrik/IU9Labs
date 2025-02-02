use master
GO

IF (
	SELECT name
	FROM sys.databases
	WHERE name = N'lab_9'
) IS NOT NULL
DROP DATABASE lab_9
GO

CREATE DATABASE lab_9
GO

use lab_9
GO

--- ƒл€ одной из таблиц пункта 2 задани€ 7 создать
--- триггеры на вставку, удаление и добавление, при
--- выполнении заданных условий один из триггеров
--- должен инициировать возникновение ошибки
--- (RAISERROR / THROW).


CREATE TABLE Doctor (
    DoctorID INT PRIMARY KEY,
    PassportNum NVARCHAR(10),
	Name NVARCHAR(50),
	Surname NVARCHAR(50),
	Middlename NVARCHAR(50),
	Specialization NVARCHAR(30),
);
GO

CREATE TABLE STATISTIC (
	DoctorID INT,
	Name NVARCHAR(50),
	Surname NVARCHAR(50),
	Middlename NVARCHAR(50),
	Statistic NVARCHAR(20),
	TimeOf DATETIME,
);
GO

CREATE TRIGGER Doctor_graduated ON Doctor
	AFTER INSERT
	AS 
	INSERT INTO STATISTIC (DoctorID, Name, Surname, Middlename, Statistic, TimeOf)
    SELECT DoctorID, Name, Surname, Middlename, 'graduated', GETDATE() 
    FROM inserted;
GO

CREATE TRIGGER Doctor_die ON Doctor
	AFTER DELETE
	AS 
	INSERT INTO STATISTIC (DoctorID, Name, Surname, Middlename, Statistic, TimeOf)
    SELECT DoctorID, Name, Surname, Middlename, 'die', GETDATE() 
    FROM deleted;
GO

CREATE TRIGGER Doctor_update  ON Doctor
	AFTER UPDATE
	AS
	BEGIN
    IF UPDATE(Name)
		BEGIN
		INSERT INTO STATISTIC (DoctorID, Name, Surname, Middlename, Statistic, TimeOf)
		SELECT DoctorID, Name, Surname, Middlename, 'Update name', GETDATE() 
		FROM deleted;
		INSERT INTO STATISTIC (DoctorID, Name, Surname, Middlename, Statistic, TimeOf)
		SELECT DoctorID, Name, Surname, Middlename, 'New name', GETDATE() 
		FROM inserted;
		END
	ELSE
		BEGIN
			RAISERROR('Ќельз€ измен€ть в таблице Doctor ничего, кроме имени', 16, 1);
			ROLLBACK TRANSACTION;
		END
END
GO


INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, Middlename, Specialization) VALUES 
(1, '4518737303', 'Alex', 'Nikitin', 'Vladimirovich', 'Pediatr'),
(2, '4518737304', 'Valera', 'Kotov', 'Vladimirovich', 'Pediatr'),
 (3, '4518737305', 'Slava', 'Fortsy', 'Vasilevich', 'Terapevt'),
  (4, '4518737306', 'Ignat', 'Shprits', 'Igorevich', 'Terapevt'),
  (5, '4518737307', 'Vasia', 'Romanov', 'Igorevich', 'Dentist'),
  (6, '4518737308', 'Igor', 'Krutoi', 'Vasilevich', 'Terapevt'),
   (7, '4518737309', 'Sergei', 'Sobolev', 'Alexeevich', 'Dentist');
GO



UPDATE Doctor SET Name = 'NoName' WHERE DoctorID < 4;
--- UPDATE Doctor SET Surname = 'NoName' WHERE DoctorID > 3; --- выдаст ошибку, тк мен€ем не Name
GO


DELETE FROM Doctor WHERE DoctorID > 4;
GO



SELECT * FROM STATISTIC;
--- SELECT * FROM Doctor;
GO

DROP TABLE Doctor;
DROP TABLE STATISTIC;
GO


--- ƒл€ представлени€ пункта 2 задани€ 7 создать
--- триггеры на вставку, удаление и добавление,
--- обеспечивающие возможность выполнени€
--- операций с данными непосредственно через
--- представление.


CREATE TABLE Doctor (
    DoctorID INT PRIMARY KEY,
    PassportNum NVARCHAR(10),
	Name NVARCHAR(50),
	Surname NVARCHAR(50),
	Middlename NVARCHAR(50),
	Specialization NVARCHAR(30),
	DiplomID INT --- дл€ реализации 1 к 1
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
	SELECT doc.DoctorID, doc.PassportNum, doc.Name, doc.Surname, doc.Middlename, doc.Specialization, 
       dip.diplomID, dip.RegistrNum, dip.DiplomDate, dip.AcademicDegree
	FROM dbo.Doctor AS doc 
	INNER JOIN dbo.Diploma AS dip ON doc.DoctorID = dip.DoctorID;
GO

INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, Middlename, Specialization, DiplomID) VALUES (1, '4518737303', 'Alex', 'Nikitin', 'Vladimirovich', 'Pediatr', 1),
(2, '4518737304', 'Valera', 'Kotov', 'Vladimirovich', 'Pediatr', 2), 
(3, '4518737305', 'Slava', 'Fortsy', 'Vasilevich', 'Terapevt', 3),
(4, '4518737306', 'Ignat', 'Shprits', 'Igorevich', 'Terapevt', 4),
(5, '4518737307', 'Vasia', 'Romanov', 'Igorevich', 'Dentist', 5),
 (6, '4518737308', 'Igor', 'Krutoi', 'Vasilevich', 'Terapevt', 6),
 (7, '4518737309', 'Sergei', 'Sobolev', 'Alexeevich', 'Dentist', 7);

INSERT INTO Diploma (diplomID, RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree, DoctorID) VALUES 
(1, 356736, 'Alex', 'Nikitin', 'Vladimirovich', '2008-07-15', 'bacalavr', 1),
 (2, 356735, 'Valera', 'Kotov', 'Vladimirovich', '2024-07-15', 'magistr', 2),
  (3, 356734, 'Slava', 'Fortsy', 'Vasilevich', '2009-07-15', 'bacalavr', 3),
   (4, 356733, 'Ignat', 'Shprits', 'Igorevich', '2021-07-15', 'magistr', 4),
    (5, 356732, 'Vasia', 'Romanov', 'Igorevich', '2018-07-15', 'bacalavr', 5),
	 (6, 356731, 'Igor', 'Krutoi', 'Vasilevich', '2000-07-15', 'magistr', 6),
	  (7, 356730, 'Sergei', 'Sobolev', 'Alexeevich', '2001-07-15', 'bacalavr', 7);
GO


CREATE TRIGGER Insert_Doctor_with_diploma_view ON Doctor_with_diploma_view
INSTEAD OF INSERT
AS
BEGIN
    INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, Middlename, Specialization, DiplomID)
    SELECT i.DoctorID, i.PassportNum, i.Name, i.Surname, i.Middlename, i.Specialization, i.diplomID
    FROM inserted i;

    
    INSERT INTO Diploma (diplomID, RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree, DoctorID)
    SELECT i.diplomID, i.RegistrNum, i.Name, i.Surname, i.Middlename, i.DiplomDate, i.AcademicDegree, i.DoctorID
    FROM inserted i;
END;
GO


CREATE TRIGGER Delete_Doctor_with_diploma_view ON Doctor_with_diploma_view
INSTEAD OF DELETE
AS
BEGIN
    DELETE FROM Diploma
    WHERE DoctorID IN (SELECT DoctorID FROM deleted);

    DELETE FROM Doctor
    WHERE DoctorID IN (SELECT DoctorID FROM deleted);
END;
GO

CREATE TRIGGER Update_Doctor_with_diploma_view ON Doctor_with_diploma_view
INSTEAD OF UPDATE
AS
BEGIN
    UPDATE Doctor
    SET 
        PassportNum = i.PassportNum,
        Name = i.Name,
        Surname = i.Surname,
        Middlename = i.Middlename,
        Specialization = i.Specialization
    FROM inserted i
    WHERE Doctor.DoctorID = i.DoctorID;

    UPDATE Diploma
    SET 
        RegistrNum = i.RegistrNum,
        Name = i.Name,
        Surname = i.Surname,
        Middlename = i.Middlename,
        DiplomDate = i.DiplomDate,
        AcademicDegree = i.AcademicDegree
    FROM inserted i
    WHERE Diploma.DoctorID = i.DoctorID;
END;
GO


SELECT * FROM Doctor;
SELECT * FROM Diploma;
SELECT * FROM Doctor_with_diploma_view;
GO

INSERT INTO Doctor_with_diploma_view (DoctorID, PassportNum, Name, Surname, Middlename, Specialization, diplomID, RegistrNum, DiplomDate, AcademicDegree)
VALUES (8, '4518090909', 'Petr', 'Petrov', 'Petrovich', 'Surgeon', 8, 654321, '2008-07-15', 'bacalavr'),
(9, '4518090909', 'Max', 'Stukov', 'Petrovich', 'Surgeon', 9, 654321, '2008-07-15', 'magistr'),
(10, '4518090909', 'Stefan', 'Alexeevich', 'Petrovich', 'Surgeon-dentist', 10, 654321, '2008-07-15', 'bacalavr'),
(11, '4518090909', 'Dmitry', 'Dmitrievich', 'Petrovich', 'Surgeon-dentist', 11, 654321, '2008-07-15', 'magistr');
GO


DELETE FROM Doctor_with_diploma_view WHERE DoctorID < 5;

UPDATE Doctor_with_diploma_view SET Name = 'New name' WHERE DoctorID > 6;

SELECT * FROM Doctor;
SELECT * FROM Diploma;
SELECT * FROM Doctor_with_diploma_view;
GO

DROP VIEW Doctor_with_diploma_view;
DROP TABLE Diploma;
DROP TABLE Doctor;
GO