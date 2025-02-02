use laba_10;
GO


---  READ UNCOMMITTED
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED; --- не блокируется
BEGIN TRANSACTION;
UPDATE Doctor SET Name = 'New Slava' WHERE DoctorID = 3; 
WAITFOR DELAY '00:00:15' 
COMMIT TRANSACTION; 



-- READ COMMITTED
SET TRANSACTION ISOLATION LEVEL READ COMMITTED; --- блокируется до окончания основной транзакции
BEGIN TRANSACTION;
UPDATE Doctor SET Name = 'New Alex' WHERE DoctorID = 1; 
COMMIT TRANSACTION;
GO




-- REPEATABLE READ
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ; --- не блокируется (фантомное чтение)
BEGIN TRANSACTION;
INSERT INTO Doctor  (DoctorID, PassportNum, Name, Surname, Middlename, Specialization) VALUES
(11, '4518737309', 'Sergei', 'Guru', 'Alexeevich', 'Dentist');
COMMIT TRANSACTION; 
GO

SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;  --- блокируется до окончания основной транзакции
BEGIN TRANSACTION;
UPDATE Doctor SET Name = 'New Valera' WHERE DoctorID = 2;
COMMIT TRANSACTION;
GO 

--- SERIALIZABLE;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE; --- блокируется до окончания основной транзакции
BEGIN TRANSACTION;
INSERT INTO Doctor  (DoctorID, PassportNum, Name, Surname, Middlename, Specialization) VALUES
(6, '4518737308', 'Igor', 'Krutoi', 'Vasilevich', 'Terapevt'),
(7, '4518737309', 'Sergei', 'Sobolev', 'Alexeevich', 'Dentist'); -- блокируется до момента окончания основной транзакции
COMMIT TRANSACTION; 