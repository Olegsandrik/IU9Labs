USE master;
GO


IF (
	SELECT name
	FROM sys.databases
	WHERE name = N'lab_11'
) IS NOT NULL
DROP DATABASE lab_11
GO

CREATE DATABASE [lab_11]
	ON ( NAME = lab_11_dat, FILENAME = 'D:\DBlabs\lab_11dat.mdf', SIZE = 10, MAXSIZE = UNLIMITED, FILEGROWTH = 5% )
	LOG ON ( NAME = lab_11_log, FILENAME = 'D:\DBlabs\lab_11log.ldf', SIZE = 5MB, MAXSIZE = 25MB, FILEGROWTH = 5MB );
GO


USE lab_11;
GO



IF OBJECT_ID(N'Diploma') is NOT NULL
    DROP TABLE Diploma;
GO

IF OBJECT_ID(N'Visit') is NOT NULL
    DROP TABLE Visit;
GO

IF OBJECT_ID(N'Doctor') is NOT NULL
    DROP TABLE Doctor;
GO

IF OBJECT_ID(N'Ministry') is NOT NULL
    DROP TABLE Ministry;
GO



IF OBJECT_ID(N'Pacient') is NOT NULL
    DROP TABLE Pacient;
GO


IF OBJECT_ID(N'Polyclinic') is NOT NULL
    DROP TABLE Polyclinic;
GO


IF OBJECT_ID(N'VisitsSTAT') is NOT NULL
    DROP TABLE DoctorsSTAT;
GO

CREATE TABLE VisitsSTAT (
	StatDateTime DATE DEFAULT GETDATE(),
	VisDate DATE NOT NULL,
	VisTime TIME NOT NULL,
	VisStatus NVARCHAR(100) NOT NULL,
	DoctorID INT NOT NULL,
	PacientID INT NOT NULL,
);
GO

CREATE TABLE Polyclinic
(
    PolyclinicID INT PRIMARY KEY,
    LicenseNum INT NOT NULL,
    BranchNum INT NOT NULL,
	AddressMin NVARCHAR(200) NULL,
    Email NVARCHAR(255) NOT NULL,
    WebsiteLink CHAR(2048) NOT NULL,
	PhoneNum NVARCHAR(11) NOT NULL
);
GO


CREATE TABLE Pacient (
	PacientID INT PRIMARY KEY,
	Policy NVARCHAR(16) NOT NULL,
	SNILS NVARCHAR(11) NOT NULL,
	Name NVARCHAR(50) NOT NULL,
	Surname NVARCHAR(50) NOT NULL,
	Middlename NVARCHAR(50) NULL,
	Height INT NOT NULL,
	Weiht INT NOT NULL,
	PolyclinicID INT,
	CONSTRAINT FK_Pacient_Polyclinic FOREIGN KEY (PolyclinicID)
        REFERENCES Polyclinic(PolyclinicID)
        ON DELETE SET NULL
);
GO

CREATE TABLE Doctor (
    DoctorID INT PRIMARY KEY,
    PassportNum NVARCHAR(10) NOT NULL,
	Name NVARCHAR(50) NOT NULL,
	Surname NVARCHAR(50) NOT NULL,
	Middlename NVARCHAR(50) NULL,
	Specialization NVARCHAR(30) NOT NULL,
);
GO



CREATE TABLE Visit(
	DirectionNum INT NOT NULL,
	VisDate DATE,
	VisTime TIME,
	Complains NVARCHAR(100),
	Appointment NVARCHAR(100),
	DoctorID INT,
    CONSTRAINT FK_Visit_Doctor FOREIGN KEY (DoctorID)
        REFERENCES Doctor(DoctorID)
        ON DELETE CASCADE,
	PolyclinicID INT,
	CONSTRAINT FK_Visit_Polyclinic FOREIGN KEY (PolyclinicId)
        REFERENCES Polyclinic(PolyclinicID)
        ON DELETE CASCADE,
	PacientID INT,
    CONSTRAINT FK_Visit_Pacient FOREIGN KEY (PacientID)
        REFERENCES Pacient(PacientID)
        ON DELETE CASCADE
);
GO


CREATE TABLE Diploma (
    DiplomID INT PRIMARY KEY,
    RegistrNum INT NOT NULL,
	Name NVARCHAR(20) NOT NULL,
	Surname NVARCHAR(20) NOT NULL,
	Middlename NVARCHAR(20),
	DiplomDate DATETIME NOT NULL,
	AcademicDegree NVARCHAR(20) NOT NULL,
    DoctorID INT,
    CONSTRAINT FK_Diploma_Doctor FOREIGN KEY (DoctorID)
        REFERENCES Doctor(DoctorID)
        ON DELETE CASCADE
);
GO


ALTER TABLE Diploma
ALTER COLUMN DiplomDate DATE;
GO

CREATE INDEX PacientIndex
	ON Pacient (Name, Surname, Middlename) 
	INCLUDE (SNILS, Policy)
GO


CREATE INDEX DoctorIndex
	ON Doctor (Name, Surname, Middlename) 
	INCLUDE (Specialization, PassportNum)
GO

CREATE VIEW Visit_view AS
SELECT 
    vis.DirectionNum,
    vis.VisDate,
    vis.VisTime,
    vis.Complains,
    vis.Appointment,
    pac.Name AS PatientName,
    pac.Surname AS PatientSurname,
    doc.Name AS DoctorName,
    doc.Surname AS DoctorSurname,
    poly.AddressMin AS PolyclinicAddress
FROM 
    Visit vis
JOIN 
    Pacient pac ON vis.PacientID = pac.PacientID
JOIN 
    Doctor doc ON vis.DoctorID = doc.DoctorID
JOIN 
    Polyclinic poly ON vis.PolyclinicID = poly.PolyclinicID;
GO


CREATE TRIGGER Insert_Visit ON Visit
	AFTER INSERT
	AS
	BEGIN
    INSERT INTO VisitsSTAT (VisDate, VisTime, VisStatus, DoctorID, PacientID)
    SELECT i.VisDate, i.VisTime, 'CREATE', i.DoctorID, i.PacientID 
    FROM inserted i;
	END;
GO


CREATE TRIGGER Delete_Visit ON Visit
	AFTER DELETE
	AS
	BEGIN
    INSERT INTO VisitsSTAT ( VisDate, VisTime, VisStatus, DoctorID, PacientID)
    SELECT i.VisDate, i.VisTime, 'CANCELED', i.DoctorID, i.PacientID 
    FROM deleted i;
	END;
GO


CREATE TRIGGER Update_Visit ON Visit
	AFTER UPDATE
	AS
	BEGIN
	DECLARE @VisDateUpdated BIT = 0;
    DECLARE @VisTimeUpdated BIT = 0;

    IF UPDATE(VisDate)
        SET @VisDateUpdated = 1;

    IF UPDATE(VisTime)
        SET @VisTimeUpdated = 1;

    IF @VisDateUpdated = 1 AND @VisTimeUpdated = 1
		BEGIN
		INSERT INTO VisitsSTAT ( VisDate, VisTime, VisStatus, DoctorID, PacientID)
		SELECT i.VisDate, i.VisTime, 'Update visit date and time', i.DoctorID, i.PacientID 
		FROM inserted i;
		END
	ELSE IF @VisTimeUpdated = 1
		BEGIN
		INSERT INTO VisitsSTAT ( VisDate, VisTime, VisStatus, DoctorID, PacientID)
		SELECT i.VisDate, i.VisTime, 'Update visit time', i.DoctorID, i.PacientID 
		FROM inserted i;
		END
	ELSE IF @VisDateUpdated = 1
		BEGIN
		INSERT INTO VisitsSTAT ( VisDate, VisTime, VisStatus, DoctorID, PacientID)
		SELECT i.VisDate, i.VisTime, 'Update visit date', i.DoctorID, i.PacientID 
		FROM inserted i;
		END
	ELSE
		BEGIN
			RAISERROR('Можно изменить только дату и время визита', 16, 1);
			ROLLBACK TRANSACTION;
		END
	END;
GO


CREATE FUNCTION dbo.MySmartSearchAlexByID
(
    @input INT
)
RETURNS int
AS
BEGIN
	DECLARE @Name NVARCHAR(50)
	SET @Name = (SELECT Name FROM Pacient WHERE PacientID = @input)
	DECLARE @ans NVARCHAR(100)
	IF @Name LIKE 'Alex%'
	BEGIN
		SET @ans = 1
	END
	ELSE IF @Name LIKE 'Sash%'
	BEGIN
		SET @ans = 1
	END
	ELSE
	BEGIN
		SET @ans = 0
	END
RETURN @ans
END
GO


CREATE PROCEDURE Statistic 
	AS
	BEGIN
	SELECT vis.*, pac.Name, pac.Surname, pac.SNILS, doc.Name as DocName, doc.Surname as DocSurname
    FROM VisitsSTAT vis
    RIGHT JOIN Pacient pac ON vis.PacientID = pac.PacientID
	RIGHT JOIN Doctor doc ON vis.DoctorID = doc.DoctorID
    WHERE dbo.MySmartSearchAlexByID(vis.PacientID) = 1
	ORDER BY DoctorID ASC
	END
GO

EXEC Statistic;


INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, Middlename, Specialization) VALUES 
(1, '4518737303', 'Alex', 'Nikitin', 'Vladimirovich', 'Pediatr'),
(2, '4518737304', 'Valera', 'Kotov', 'Vladimirovich', 'Pediatr'),
 (3, '4518737305', 'Slava', 'Fortsy', 'Vasilevich', 'Terapevt'),
  (4, '4518737306', 'Ignat', 'Shprits', 'Igorevich', 'Terapevt'),
  (5, '4518737307', 'Vasia', 'Romanov', 'Igorevich', 'Dentist'),
  (6, '4518737308', 'Igor', 'Krutoi', 'Vasilevich', 'Terapevt'),
   (7, '4518737309', 'Sergei', 'Sobolev', 'Alexeevich', 'Dentist');
GO


INSERT INTO Diploma (diplomID, RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree, DoctorID) VALUES 
(1, 356736, 'Alex', 'Nikitin', 'Vladimirovich', '2008-07-15', 'bacalavr', 1),
 (2, 356735, 'Valera', 'Kotov', 'Vladimirovich', '2024-07-15', 'magistr', 2),
  (3, 356734, 'Slava', 'Fortsy', 'Vasilevich', '2009-07-15', 'bacalavr', 3),
   (4, 356733, 'Ignat', 'Shprits', 'Igorevich', '2021-07-15', 'magistr', 4),
    (5, 356732, 'Vasia', 'Romanov', 'Igorevich', '2018-07-15', 'bacalavr', 5),
	 (6, 356731, 'Igor', 'Krutoi', 'Vasilevich', '2000-07-15', 'magistr', 6),
	  (7, 356730, 'Sergei', 'Sobolev', 'Alexeevich', '2001-07-15', 'bacalavr', 7);
GO



INSERT INTO Polyclinic (PolyclinicID, LicenseNum, BranchNum, AddressMin, Email, WebsiteLink, PhoneNum)
VALUES 
(1, 123456, 1, 'Sklifasovsky 4', 'sklif@yandex.ru', 'https://sklif.ru', '79037783333'),
(2, 234567, 2, 'Buanova 6', 'Buanova@yandex.ru', 'https://buanova.ru', '79057783333'),
(3, 345678, 1, 'Morozovskaya 18', 'Morozovskaya@yandex.ru', 'https://morozovskaya.ru', '74957783333'),
(4, 456789, 3, 'Baumanskaya 3', 'bmstu@yandex.ru', 'https://bmstu.ru', '74957777033'),
(5, 567890, 2, 'Vinogradova 7', 'vinograd@yandex.ru', 'https://vinograd.ru', '79056223089');


INSERT INTO Pacient (PacientID, Policy, SNILS, Name, Surname, Middlename, Height, Weiht, PolyclinicID)
VALUES 
(1, '1234567890123456', '12345678901', 'Alex', 'Ivanov', 'Petrovich', 180, 75, 1),
(2, '2345678901234567', '98765432102', 'Petr', 'Alexeev', 'Alexandrovich', 175, 70, 2),
(3, '3456789012345678', '45678912303', 'Alexandra', 'Sidorova', 'Georgievna', 165, 60, 1),
(4, '4567890123456789', '32165498704', 'Sasha', 'Kusnetsova', 'Sergeevna', 170, 65, 3),
(5, '5678901234567890', '65432198705', 'Dmirty', 'Smirnov', 'Victorovich', 182, 80, 2),
(6, '5633901234567890', '65332198705', 'Dmirty', 'Qubov', 'Petrovich', 182, 80, 2);

INSERT INTO Visit (DirectionNum, VisDate, VisTime, Complains, Appointment, DoctorID, PolyclinicID, PacientID)
VALUES 
(134, '2023-01-01', '09:00', 'head pain', 'Консультация', 1, 1, 1),
(232, '2020-03-12', '10:30', 'knee pain', 'Обследование', 2, 2, 2),
(332, '2016-04-03', '11:15', 'cough', 'Лечение', 3, 1, 3),
(4183, '2024-11-24', '14:00', 'allergy', 'Консультация', 4, 3, 4),
(1245, '2023-10-30', '20:30', 'teeth pain', 'Консультация', 5, 2, 5),
(1212, '2020-11-30', '17:30', 'teeth pain', 'Консультация', 5, 2, 3);

UPDATE Visit
SET VisDate = '2023-03-12'
WHERE DirectionNum = 232;


UPDATE Visit
SET VisTime = '12:00'
WHERE DirectionNum = 332;

UPDATE Visit
SET VisTime = '12:00', VisDate = '2023-03-12'
WHERE DirectionNum = 332;

DELETE FROM Visit
WHERE DirectionNum = 4183;

DELETE FROM Visit
WHERE DirectionNum = 332;

EXEC Statistic;

--- дополнительно для выполнения ТЗ лабы

SELECT DISTINCT Name AS PersonName FROM Pacient WHERE PacientID BETWEEN 1 and 10 
UNION --- удалит дубликаты
SELECT DISTINCT Name FROM Doctor WHERE DoctorID IN (1,2,3,4,5,6,7,8,9);
GO

SELECT DISTINCT Name AS PersonName FROM Pacient WHERE PacientID BETWEEN 1 and 10 
UNION ALL --- не удалит
SELECT DISTINCT Name FROM Doctor WHERE DoctorID IN (1,2,3,4,5,6,7,8,9);
GO

SELECT DISTINCT Name AS PersonName FROM Pacient WHERE PacientID BETWEEN 1 and 10 
EXCEPT --- возвращает строки из первого запроса, которые не присутствуют во втором запросе.
SELECT DISTINCT Name FROM Doctor WHERE DoctorID IN (1,2,3,4,5,6,7,8,9);
GO

SELECT DISTINCT Name AS PersonName FROM Pacient WHERE PacientID BETWEEN 1 and 10 
INTERSECT --- возвращает строки, которые присутствуют в обоих запросах.
SELECT DISTINCT Name FROM Doctor WHERE DoctorID IN (1,2,3,4,5,6,7,8,9);
GO


SELECT 
    doc.Name AS DoctorName,
    doc.Surname AS DoctorSurname,
    COUNT(vis.DirectionNum) AS TotalVisits
FROM 
    Doctor doc
RIGHT JOIN 
    Visit vis ON doc.DoctorID = vis.DoctorID
GROUP BY 
    doc.Name, doc.Surname
HAVING 
    COUNT(vis.DirectionNum) > 0;
GO


SELECT Name, Surname
FROM Pacient
WHERE PacientID IN (
    SELECT PacientID
    FROM Visit
    WHERE DoctorID in (SELECT DoctorID FROM Doctor WHERE Name = 'Alex' AND Surname = 'Nikitin')
);
GO

SELECT * FROM Pacient WHERE Name is Null
GO

IF EXISTS (SELECT * FROM Pacient WHERE Name LIKE 'Alex')
BEGIN
PRINT('Нашелся Сашек')
END
GO

SELECT 
    doc.Name AS DoctorName,
    doc.Surname AS DoctorSurname,
    COUNT(vis.DirectionNum) AS TotalVisits
FROM 
    Doctor doc
LEFT JOIN 
    Visit vis ON doc.DoctorID = vis.DoctorID
GROUP BY 
    doc.Name, doc.Surname
HAVING 
    MIN(vis.DirectionNum) > 0;
GO

SELECT 
    doc.Name AS DoctorName,
    doc.Surname AS DoctorSurname,
    COUNT(vis.DirectionNum) AS TotalVisits
FROM 
    Doctor doc
FULL OUTER JOIN 
    Visit vis ON doc.DoctorID = vis.DoctorID
GROUP BY 
    doc.Name, doc.Surname
HAVING 
    AVG(vis.DirectionNum) > 3;
GO


SELECT 
    doc.Name AS DoctorName,
    doc.Surname AS DoctorSurname,
    COUNT(vis.DirectionNum) AS TotalVisits
FROM 
    Doctor doc
INNER JOIN 
    Visit vis ON doc.DoctorID = vis.DoctorID
GROUP BY 
    doc.Name, doc.Surname
HAVING 
    MAX(vis.DirectionNum) < 10;
GO

SELECT vis.*, pac.Name, pac.Surname, pac.SNILS, doc.Name as DocName, doc.Surname as DocSurname
    FROM VisitsSTAT vis
    RIGHT JOIN Pacient pac ON vis.PacientID = pac.PacientID
	RIGHT JOIN Doctor doc ON vis.DoctorID = doc.DoctorID
    WHERE dbo.MySmartSearchAlexByID(vis.PacientID) = 1
	ORDER BY DoctorID DESC
GO

DROP FUNCTION dbo.MySmartSearchAlexByID
DROP PROCEDURE Statistic;
DROP TRIGGER Update_Visit, Insert_Visit, Delete_Visit;
GO

DROP VIEW Visit_View
GO

DROP INDEX PacientIndex ON Pacient;
GO

DROP INDEX DoctorIndex ON Doctor;
GO
