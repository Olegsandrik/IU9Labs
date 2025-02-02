use master
GO

IF (
	SELECT name
	FROM sys.databases
	WHERE name = N'lab_8'
) IS NOT NULL
DROP DATABASE lab_8
GO

CREATE DATABASE lab_8
GO

use lab_8
GO

CREATE TABLE Pacient (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
	SNILS NVARCHAR(11) NOT NULL,
	Email NVARCHAR(255) NOT NULL,
);
GO


INSERT INTO Pacient(Name, SNILS, Email) VALUES ('Alexa', '12345678900', 'Alex@mail.ru');
INSERT INTO Pacient(Name, SNILS, Email) VALUES ('Igor', '12345678900', 'Igor@mail.ru');
INSERT INTO Pacient(Name, SNILS, Email) VALUES ('Vova', '12345678901', 'Vova@mail.ru');
INSERT INTO Pacient(Name, SNILS, Email) VALUES ('Ignat', '12345678904', 'Ignat@mail.ru');
GO

--- Создать хранимую процедуру, производящую выборку
--- из некоторой таблицы и возвращающую результат
--- выборки в виде курсора.

CREATE PROCEDURE GetPacientsCursor1 
	@firstname varchar(20) = '%a%',	--- параметр
	@cursor CURSOR VARYING OUTPUT --- выходной параметр
AS
	SET @cursor = CURSOR FORWARD_ONLY STATIC FOR 
		SELECT ID, Email, Name, SNILS
		FROM Pacient
		WHERE Name LIKE @firstname;
	OPEN @cursor;
GO

DECLARE @pacientCursor CURSOR;
EXEC GetPacientsCursor1 @cursor = @pacientCursor OUTPUT; --  передает курсор в переменную @pacientCursor как выходной параметр

FETCH NEXT FROM @pacientCursor;
WHILE (@@FETCH_STATUS = 0)
	BEGIN
		FETCH NEXT FROM @pacientCursor;
	END

CLOSE @pacientCursor ;
DEALLOCATE @pacientCursor ;
GO


--- Модифицировать хранимую процедуру п.1. таким
--- образом, чтобы выборка осуществлялась с
--- формированием столбца, значение которого
--- формируется пользовательской функцией.


CREATE FUNCTION dbo.MyReverse
(
    @input NVARCHAR(100)
)
RETURNS NVARCHAR(100)
AS
BEGIN
	DECLARE @ans NVARCHAR(100)
	IF ISNUMERIC(@input) = 1 AND LEN(@input) < 5
	BEGIN
		SET @ans = CAST(CAST(@input AS float)*2 AS NVARCHAR(100))
	END
	ELSE
	BEGIN
		SET @ans = REVERSE(@input);
	END
RETURN @ans
END
GO

CREATE PROCEDURE GetPacientsCursor 
	@firstname varchar(20) = '%a%',	--- параметр
	@cursor CURSOR VARYING OUTPUT --- выходной параметр
AS
	SET @cursor = CURSOR FORWARD_ONLY STATIC FOR 
		SELECT dbo.MyReverse(ID) as DoubleID, dbo.MyReverse(Email) as ReversEmail, dbo.MyReverse(Name) as ReversName, dbo.MyReverse(SNILS) as  ReversSNILS
		FROM Pacient
		WHERE Name LIKE @firstname;
	OPEN @cursor;
GO

DECLARE @pacientCursor CURSOR;
EXEC GetPacientsCursor @cursor = @pacientCursor OUTPUT; --  передает курсор в переменную @pacientCursor как выходной параметр


FETCH NEXT FROM @pacientCursor;
WHILE (@@FETCH_STATUS = 0)
	BEGIN
		FETCH NEXT FROM @pacientCursor;
	END

CLOSE @pacientCursor ;
DEALLOCATE @pacientCursor ;
GO




--- Создать хранимую процедуру, вызывающую процедуру
--- п.1., осуществляющую прокрутку возвращаемого
--- курсора и выводящую сообщения, сформированные из
--- записей при выполнении условия, заданного еще одной
--- пользовательской функцией.


CREATE FUNCTION dbo.MySearchA
(
    @input NVARCHAR(100)
)
RETURNS int
AS
BEGIN
	DECLARE @ans NVARCHAR(100)
	IF @input LIKE 'A%'
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

CREATE PROCEDURE GetPacientsWithA 
AS
	DECLARE @pacientCursor CURSOR;
	DECLARE @Name NVARCHAR(100);
	DECLARE @Email NVARCHAR(255);
	DECLARE @SNILS NVARCHAR(11);
	DECLARE @ID INT;

	EXEC GetPacientsCursor1 @cursor = @pacientCursor OUTPUT; --  передает курсор в переменную @pacientCursor как выходной параметр

	FETCH NEXT FROM @pacientCursor INTO @ID, @Email, @Name, @SNILS;
	WHILE (@@FETCH_STATUS = 0)
	BEGIN
		IF dbo.MySearchA(@Name)=1
		BEGIN
			PRINT 'Email: ' + @Email + ', Name: ' + @Name + ', SNILS: ' + @SNILS + ' Нашли имя начинающееся А';
			FETCH NEXT FROM @pacientCursor INTO @ID, @Email, @Name, @SNILS;
		END
		ELSE
		BEGIN
			FETCH NEXT FROM @pacientCursor INTO @ID, @Email, @Name, @SNILS;
		END
	END

	CLOSE @pacientCursor ;
	DEALLOCATE @pacientCursor ;
GO

EXEC GetPacientsWithA;
DROP FUNCTION dbo.MySearchA;
GO



--- Модифицировать хранимую процедуру п.2. таким
--- образом, чтобы выборка формировалась с помощью
--- табличной функции.



CREATE FUNCTION dbo.MySearchByA()
RETURNS TABLE
RETURN (
	SELECT ID, Name, SNILS, Email FROM Pacient WHERE Name LIKE '%a%'
)
GO


CREATE FUNCTION dbo.MySearchByID(@input INT)
RETURNS @ResultTable TABLE(ID INT, Email NVARCHAR(255), Name NVARCHAR(100), SNILS NVARCHAR(11))
AS
BEGIN
	INSERT INTO @ResultTable
	SELECT ID,  Email, Name, SNILS FROM Pacient
	WHERE ID = @input

	RETURN
END;
GO

CREATE PROCEDURE GetPacientsCursor4_1
	@cursor CURSOR VARYING OUTPUT --- выходной параметр
AS
	SET @cursor = CURSOR FORWARD_ONLY STATIC FOR 
		SELECT ID, Email, Name, SNILS
		FROM dbo.MySearchByID(2)
	OPEN @cursor;
GO


DECLARE @pacientCursor2 CURSOR;
EXEC GetPacientsCursor4_1 @cursor = @pacientCursor2 OUTPUT; --  передает курсор в переменную @pacientCursor как выходной параметр


FETCH NEXT FROM @pacientCursor2;
WHILE (@@FETCH_STATUS = 0)
	BEGIN
		FETCH NEXT FROM @pacientCursor2;
	END

CLOSE @pacientCursor2 ;
DEALLOCATE @pacientCursor2 ;
GO

CREATE PROCEDURE GetPacientsCursor4 
	@cursor CURSOR VARYING OUTPUT --- выходной параметр
AS
	SET @cursor = CURSOR FORWARD_ONLY STATIC FOR 
		SELECT dbo.MyReverse(ID) as DoubleID, dbo.MyReverse(Email) as ReversEmail, dbo.MyReverse(Name) as ReversName, dbo.MyReverse(SNILS) as  ReversSNILS
		FROM dbo.MySearchByA()
	OPEN @cursor;
GO



DECLARE @pacientCursor CURSOR;
EXEC GetPacientsCursor4 @cursor = @pacientCursor OUTPUT; --  передает курсор в переменную @pacientCursor как выходной параметр


FETCH NEXT FROM @pacientCursor;
WHILE (@@FETCH_STATUS = 0)
	BEGIN
		FETCH NEXT FROM @pacientCursor;
	END

CLOSE @pacientCursor ;
DEALLOCATE @pacientCursor ;
GO


DROP TABLE Pacient;
GO
DROP PROCEDURE GetPacientsCursor1;
DROP PROCEDURE GetPacientsCursor;
DROP PROCEDURE GetPacientsCursor4;
GO

DROP FUNCTION dbo.MyReverse, dbo.MySearchByA;
GO