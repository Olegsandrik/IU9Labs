USE master;
GO

IF  EXISTS (
    SELECT name
    FROM sys.databases
    WHERE name = N'laba_10'
)
BEGIN
    ALTER DATABASE laba_10 SET SINGLE_USER WITH ROLLBACK IMMEDIATE; --- для отката всех транзакций и управления одного пользователя
    DROP DATABASE laba_10;
END
GO

CREATE DATABASE laba_10;
GO

USE laba_10;
GO

CREATE TABLE Doctor (
    DoctorID INT PRIMARY KEY,
    PassportNum NVARCHAR(10),
	Name NVARCHAR(50),
	Surname NVARCHAR(50),
	Middlename NVARCHAR(50),
	Specialization NVARCHAR(30),
);
GO


INSERT INTO Doctor (DoctorID, PassportNum, Name, Surname, Middlename, Specialization) VALUES 
(1, '4518737303', 'Alex', 'Nikitin', 'Vladimirovich', 'Pediatr'),
(2, '4518737304', 'Valera', 'Kotov', 'Vladimirovich', 'Pediatr'),
 (3, '4518737305', 'Slava', 'Fortsy', 'Vasilevich', 'Terapevt'),
  (4, '4518737306', 'Ignat', 'Shprits', 'Igorevich', 'Terapevt'),
  (5, '4518737307', 'Vasia', 'Romanov', 'Igorevich', 'Dentist');
GO


---  READ UNCOMMITTED (возможно грязное чтение, невоспроизводимое чтение, фантомное чтение)
--- Демонстрация грязного чтения
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN TRANSACTION;
SELECT * FROM Doctor WHERE DoctorID = 3;
WAITFOR DELAY '00:00:10'
SELECT * FROM Doctor WHERE DoctorID = 3; -- новое имя появится, тк можно читать грязные данные
COMMIT TRANSACTION;
GO




--- READ COMMITTED (возможно невоспроизводимое чтение, фантомное чтение)
--- Демонстрация невоспроизводимого чтения
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRANSACTION;
SELECT * FROM Doctor WHERE DoctorID = 1;
WAITFOR DELAY '00:00:15' 
SELECT * FROM Doctor WHERE DoctorID = 1;
COMMIT TRANSACTION; 
GO



--- REPEATABLE READ (возможно фантомное чтение)
--- демонстрация фантомного чтения
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN TRANSACTION;
SELECT * FROM Doctor WHERE DoctorID = 2;
WAITFOR DELAY '00:00:10'
SELECT * FROM Doctor;  -- новое имя у доктора не появится, тк есть гарантия неизменности читаемых данных, но новый доктор появится
COMMIT TRANSACTION;
GO



--- SERIALIZABLE (нет проблем изоляции)
--- демонстрация работы с блокировкой
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN TRANSACTION;
SELECT * FROM Doctor
WAITFOR DELAY '00:00:10';
SELECT * FROM Doctor
COMMIT TRANSACTION;
GO


SELECT * FROM sys.dm_tran_locks;
DROP TABLE Doctor
GO