USE lab13_first
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

USE lab13_second
GO

CREATE TABLE Diploma (
    DiplomID INT PRIMARY KEY,
    RegistrNum INT NOT NULL,
	Name NVARCHAR(20) NOT NULL,
	Surname NVARCHAR(20) NOT NULL,
	Middlename NVARCHAR(20),
	DiplomDate DATE NOT NULL,
	AcademicDegree NVARCHAR(20) NOT NULL,
    DoctorID INT
);
GO

CREATE TRIGGER DiplomaUpdate ON Diploma
FOR update
AS
BEGIN
	IF UPDATE(DoctorID)
	BEGIN
	RAISERROR('Операция обновления DoctorID у Diploma невозможна и была отменена', 16, 1);
	ROLLBACK TRANSACTION
	END
END
GO


CREATE TRIGGER DiplomaInsert ON Diploma
FOR INSERT
AS
BEGIN
	DECLARE @count int
	SET @count = (SELECT COUNT(*) FROM (SELECT i.DoctorID FROM inserted i EXCEPT SELECT i.DoctorID FROM inserted i WHERE i.DoctorID IN  (SELECT DoctorID FROM lab13_first.dbo.Doctor)) as diff)
    IF @count = 0
	BEGIN
        RETURN;
    END
    ELSE
    BEGIN
        RAISERROR('Операция записи Diploma с несуществующим DoctorID невозможна и была отменена', 16, 1);
        ROLLBACK TRANSACTION;
    END
END
GO


USE lab13_first
GO


CREATE TRIGGER DoctorUpdate ON Doctor
FOR UPDATE
AS
BEGIN
    IF UPDATE(DoctorID)
    BEGIN
        RAISERROR('Операция обновления DoctorID у Doctor невозможна и была отменена', 16, 1);
        ROLLBACK TRANSACTION;
    END
END
GO

CREATE TRIGGER DoctorDelete ON Doctor
FOR Delete
AS
BEGIN
	DELETE FROM lab13_second.dbo.Diploma WHERE DoctorID in (SELECT DoctorID FROM deleted)
END
GO


INSERT INTO lab13_first.dbo.Doctor (DoctorID, PassportNum, Name, Surname, Middlename, Specialization) VALUES 
(1, '4518737303', 'Alex', 'Nikitin', 'Vladimirovich', 'Pediatr'),
(2, '4518737304', 'Valera', 'Kotov', 'Vladimirovich', 'Pediatr'),
 (3, '4518737305', 'Slava', 'Fortsy', 'Vasilevich', 'Terapevt'),
  (4, '4518737306', 'Ignat', 'Shprits', 'Igorevich', 'Terapevt'),
  (5, '4518737307', 'Vasia', 'Romanov', 'Igorevich', 'Dentist'),
  (6, '4518737308', 'Igor', 'Krutoi', 'Vasilevich', 'Terapevt'),
   (7, '4518737309', 'Sergei', 'Sobolev', 'Alexeevich', 'Dentist');
GO

INSERT INTO lab13_second.dbo.Diploma (diplomID, RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree, DoctorID) VALUES 
(1, 356736, 'Alex', 'Nikitin', 'Vladimirovich', '2008-07-15', 'bacalavr', 1),
(2, 356735, 'Valera', 'Kotov', 'Vladimirovich', '2024-07-15', 'magistr', 2),
(3, 356734, 'Slava', 'Fortsy', 'Vasilevich', '2009-07-15', 'bacalavr', 3),
(4, 356733, 'Ignat', 'Shprits', 'Igorevich', '2021-07-15', 'magistr', 4),
(5, 356732, 'Vasia', 'Romanov', 'Igorevich', '2018-07-15', 'bacalavr', 5),
(6, 356731, 'Igor', 'Krutoi', 'Vasilevich', '2000-07-15', 'magistr', 6),
(7, 356730, 'Sergei', 'Sobolev', 'Alexeevich', '2001-07-15', 'bacalavr', 7);
GO


-- INSERT INTO lab13_second.dbo.Diploma (diplomID, RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree, DoctorID) VALUES 
-- (8, 356730, 'Sasha', 'Sobolev', 'Igorevich', '2003-04-25', 'bacalavr', 18);
-- GO


SELECT * FROM lab13_second.dbo.Diploma
SELECT * FROM lab13_first.dbo.Doctor
GO

DELETE lab13_first.dbo.Doctor WHERE DoctorID > 5
GO

SELECT * FROM lab13_second.dbo.Diploma
SELECT * FROM lab13_first.dbo.Doctor
GO

-- UPDATE lab13_first.dbo.Doctor SET DoctorID = 20 WHERE DoctorID = 3  
-- UPDATE lab13_second.dbo.Diploma SET DoctorID = 20 WHERE DoctorID = 3
UPDATE lab13_first.dbo.Doctor SET Name = 'NEW NAME' WHERE DoctorID < 3  
GO

SELECT * FROM lab13_second.dbo.Diploma
SELECT * FROM lab13_first.dbo.Doctor
GO

USE lab13_first
DROP TABLE Doctor
GO

USE lab13_second
DROP TABLE Diploma
GO