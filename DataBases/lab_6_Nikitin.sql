-- Задача: 1 Создать таблицу с автоинкрементным первичным
-- ключом. Изучить функции, предназначенные для
-- получения сгенерированного значения IDENTITY.

-- 2 Добавить поля, для которых используются
-- ограничения (CHECK), значения по умолчанию
-- (DEFAULT), также использовать встроенные
-- функции для вычисления значений.

-- 3 Создать таблицу с первичным ключом на основе
-- глобального уникального идентификатора.

-- 4 Создать таблицу с первичным ключом на основе
-- последовательности.

-- 5 Создать две связанные таблицы, и протестировать
-- на них различные варианты действий для
-- ограничений ссылочной целостности (NO ACTION |
-- CASCADE | SET | SET DEFAULT).

use master
GO

IF (
	SELECT name
	FROM sys.databases
	WHERE name = N'lab_6_Nikitin'
) IS NOT NULL
DROP DATABASE lab_6_Nikitin
GO

CREATE DATABASE lab_6_Nikitin
GO

use lab_6_Nikitin

-- 1 Создать таблицу с автоинкрементным первичным
-- ключом. Изучить функции, предназначенные для
-- получения сгенерированного значения IDENTITY.


CREATE TABLE Pacient (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
	SNILS NVARCHAR(11) NOT NULL,
);
GO


INSERT INTO Pacient(Name, SNILS) VALUES ('Alex', '12345678900');
INSERT INTO Pacient(Name, SNILS) VALUES ('Igor', '12345678900');
SELECT * FROM Pacient;

-- Получение сгенерированного значения IDENTITY
DECLARE @NewID INT; -- Создание переменной
INSERT INTO Pacient(Name, SNILS) VALUES ('VALDIMIR', '12345678900');
SET @NewID = SCOPE_IDENTITY(); -- возвращает последнее значение, сгенерированное для столбца с автоинкрементом в текущем контексте @@IDENTITY -- ласт зн id; 
-- SELECT IDENT_CURRENT('Pacient') as PacientID_current последний вставленный в принципе в таблицу от любого пользователя
SELECT @NewID AS GeneratedID;

DROP TABLE Pacient;

-- 2 Добавить поля, для которых используются
-- ограничения (CHECK), значения по умолчанию
-- (DEFAULT), также использовать встроенные
-- функции для вычисления значений. 

CREATE TABLE Pacient (
    ID INT IDENTITY(1,1) PRIMARY KEY,
	name NVARCHAR(20),
    hight INT CHECK (hight <= 225) DEFAULT 220,
	myweight INT CHECK (myweight <= 200) DEFAULT 100,
    bornAt DATETIME DEFAULT GETDATE()
);

INSERT INTO Pacient (Name, hight) VALUES ('Pavel', 198)
INSERT INTO Pacient (Name) VALUES ('Max')
-- INSERT INTO Pacient (Name, hight) VALUES ('Victor', 233)
SELECT * FROM Pacient;
DROP TABLE Pacient;

-- 3 Создать таблицу с первичным ключом на основе
-- глобального уникального идентификатора.
CREATE TABLE Ministry (
    IDMinisty UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
    location NVARCHAR(50) NOT NULL,
    phoneNum NVARCHAR(11) NOT NULL,
	addressMin NVARCHAR(200) NULL,
    email NVARCHAR(255) NOT NULL,
    websiteLink CHAR(2048) NOT NULL,
);

INSERT INTO Ministry (location, phoneNum, addressMin, email, websitelink) VALUES ('Moscow', '79037783633', 'Sevanskaia 33', 'MosMin@mail.com', 'https://MosMin.com');
INSERT INTO Ministry (location, phoneNum, addressMin, email, websitelink) VALUES ('Piter', '79887783633', 'Kievskaya 33', 'PiterMin@mail.com', 'https://PiterMin.com');
SELECT * FROM Ministry;
DROP TABLE Ministry;

-- 4 Создать таблицу с первичным ключом на основе
-- последовательности.
CREATE SEQUENCE Diplom AS INT START WITH 1 INCREMENT BY 1;

CREATE TABLE Diploms (
    ID INT PRIMARY KEY DEFAULT NEXT VALUE FOR Diplom,
    IDDoctor INT DEFAULT 1,
	RegistrNum INT NOT NULL,
	Name NVARCHAR(20) NOT NULL,
	Surname NVARCHAR(20) NOT NULL,
	Middlename NVARCHAR(20) NOT NULL,
	DiplomDate DATE NOT NULL,
	AcademicDegree NVARCHAR(20) NOT NULL,
);

INSERT INTO Diploms(RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree) VALUES ('13455845', 'Alex', 'Nikitin', 'Vladimirovich', '15.09.2024', 'ordinat');
INSERT INTO Diploms(RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree) VALUES ('13455', 'Alex', 'Nikitin', 'Vladimirovich', '15.3.2014', 'bakalavr');
INSERT INTO Diploms(RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree) VALUES ('13454535', 'Alex', 'Nikitin', 'Vladimirovich', '15.09.2020', 'magistr');

SELECT * FROM Diploms;

DROP TABLE Diploms;
DROP SEQUENCE Diplom;
-- 5 Создать две связанные таблицы, и протестировать
-- на них различные варианты действий для
-- ограничений ссылочной целостности (NO ACTION |
-- CASCADE | SET | SET DEFAULT).

-- Cascade
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

INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, MiddleName, Specialization) VALUES (1, '4518737303', 'Alex', 'Nikitin', 'Vladimirovich', 'Pediatr');
INSERT INTO Diploma (diplomID, RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree, DoctorID) VALUES (1, '356736', 'Alex', 'Nikitin', 'Vladimirovich', '15.7.2008', 'bacalavr', 1);

DELETE FROM Doctor WHERE DoctorID = 1;

SELECT * FROM Diploma;
DROP TABLE Diploma, Doctor;


-- NO ACTION
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
        ON DELETE NO ACTION
);

INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, MiddleName, Specialization) VALUES (1, '4518737303', 'Alex', 'Nikitin', 'Vladimirovich', 'Pediatr');
INSERT INTO Diploma (diplomID, RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree, DoctorID) VALUES (1, '356736', 'Alex', 'Nikitin', 'Vladimirovich', '15.7.2008', 'bacalavr', 1);

DELETE FROM Doctor WHERE DoctorID = 1; -- Выдает ошибку, так как ON DELETE NO ACTION

SELECT * FROM Diploma;
DROP TABLE Diploma, Doctor;

-- SET DEFAULT

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
    DoctorID INT DEFAULT 144, -- default значение
    CONSTRAINT FK_Child_Parent FOREIGN KEY (DoctorID)
        REFERENCES Doctor(DoctorID)
        ON DELETE SET DEFAULT
);

INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, MiddleName, Specialization) VALUES (1, '4518737303', 'Alex', 'Nikitin', 'Vladimirovich', 'Pediatr');
INSERT INTO Diploma (diplomID, RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree, DoctorID) VALUES (1, '356736', 'Alex', 'Nikitin', 'Vladimirovich', '15.7.2008', 'bacalavr', 1);
INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, MiddleName, Specialization) VALUES (144, '4518737303', 'Alex', 'Nikitin', 'Vladimirovich', 'Pediatr');
DELETE FROM Doctor WHERE DoctorID = 1;

SELECT * FROM Diploma;
DROP TABLE Diploma, Doctor;

-- SET NULL
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
        ON DELETE SET NULL
);

INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, MiddleName, Specialization) VALUES (1, '4518737303', 'Alex', 'Nikitin', 'Vladimirovich', 'Pediatr');
INSERT INTO Diploma (diplomID, RegistrNum, Name, Surname, Middlename, DiplomDate, AcademicDegree, DoctorID) VALUES (1, '356736', 'Alex', 'Nikitin', 'Vladimirovich', '15.7.2008', 'bacalavr', 1);

SELECT * FROM Diploma;
DROP TABLE Diploma, Doctor;