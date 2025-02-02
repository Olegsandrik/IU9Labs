USE master;
GO

IF  EXISTS (
    SELECT name
    FROM sys.databases
    WHERE name = N'laba_10'
)
BEGIN
    ALTER DATABASE laba_10 SET SINGLE_USER WITH ROLLBACK IMMEDIATE; --- ��� ������ ���� ���������� � ���������� ������ ������������
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


---  READ UNCOMMITTED (�������� ������� ������, ����������������� ������, ��������� ������)
--- ������������ �������� ������
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN TRANSACTION;
SELECT * FROM Doctor WHERE DoctorID = 3;
WAITFOR DELAY '00:00:10'
SELECT * FROM Doctor WHERE DoctorID = 3; -- ����� ��� ��������, �� ����� ������ ������� ������
COMMIT TRANSACTION;
GO




--- READ COMMITTED (�������� ����������������� ������, ��������� ������)
--- ������������ ������������������ ������
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRANSACTION;
SELECT * FROM Doctor WHERE DoctorID = 1;
WAITFOR DELAY '00:00:15' 
SELECT * FROM Doctor WHERE DoctorID = 1;
COMMIT TRANSACTION; 
GO



--- REPEATABLE READ (�������� ��������� ������)
--- ������������ ���������� ������
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN TRANSACTION;
SELECT * FROM Doctor WHERE DoctorID = 2;
WAITFOR DELAY '00:00:10'
SELECT * FROM Doctor;  -- ����� ��� � ������� �� ��������, �� ���� �������� ������������ �������� ������, �� ����� ������ ��������
COMMIT TRANSACTION;
GO



--- SERIALIZABLE (��� ������� ��������)
--- ������������ ������ � �����������
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