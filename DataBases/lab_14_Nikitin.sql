USE lab13_first;
GO

CREATE TABLE Polyclinica
(
    PolyclinicID INT PRIMARY KEY,
    LicenseNum INT NOT NULL,
    BranchNum INT NOT NULL,
	AddressMin NVARCHAR(200) NULL
);
GO

USE lab13_second;
GO


CREATE TABLE Polyclinica
(
    PolyclinicID INT PRIMARY KEY,
    Email NVARCHAR(255) NOT NULL,
    WebsiteLink CHAR(2048) NOT NULL,
	PhoneNum NVARCHAR(11) NOT NULL
);
GO

CREATE VIEW PolyclinicaVIEW AS
	SELECT first_one.PolyclinicID, first_one.LicenseNum, first_one.BranchNum, first_one.AddressMin,
	second_one.Email, second_one.WebsiteLink, second_one.PhoneNum
	FROM lab13_first.dbo.Polyclinica first_one, lab13_second.dbo.Polyclinica as second_one
	WHERE first_one.PolyclinicID = second_one.PolyclinicID
GO

CREATE TRIGGER PolyclinicaVIEWInsert ON PolyclinicaVIEW INSTEAD OF INSERT
AS
BEGIN
    INSERT INTO lab13_first.dbo.Polyclinica(PolyclinicID, LicenseNum, BranchNum, AddressMin)
    SELECT PolyclinicID, LicenseNum, BranchNum, AddressMin FROM inserted;

    INSERT INTO lab13_second.dbo.Polyclinica(PolyclinicID, Email, WebsiteLink, PhoneNum)
    SELECT PolyclinicID, Email, WebsiteLink, PhoneNum FROM inserted;
END
GO

INSERT INTO PolyclinicaVIEW(PolyclinicID, LicenseNum, BranchNum, AddressMin, Email, WebsiteLink, PhoneNum)
VALUES 
(1, 123456, 1, 'Sklifasovsky 4', 'sklif@yandex.ru', 'https://sklif.ru', '79037783333'),
(2, 234567, 2, 'Buanova 6', 'Buanova@yandex.ru', 'https://buanova.ru', '79057783333'),
(3, 345678, 1, 'Morozovskaya 18', 'Morozovskaya@yandex.ru', 'https://morozovskaya.ru', '74957783333'),
(4, 456789, 3, 'Baumanskaya 3', 'bmstu@yandex.ru', 'https://bmstu.ru', '74957777033'),
(5, 567890, 2, 'Vinogradova 7', 'vinograd@yandex.ru', 'https://vinograd.ru', '79056223989'),
(6, 123456, 1, 'Lubanka 2', 'lubanka@yandex.ru', 'https://lubanka.ru', '79037783339'),
(7, 234567, 2, 'Sevanskaya 6', 'sevanskaya@yandex.ru', 'https://sevanskaya.ru', '79057783393'),
(8, 345678, 1, 'Erevanskaya 18', 'Erevanskaya@yandex.ru', 'https://Erevanskaya.ru', '74957786333'),
(9, 456789, 3, 'Kolomenskaya 3', 'Kolomenskaya@yandex.ru', 'https://Kolomenskaya.ru', '74957777233'),
(10, 567890, 2, 'Prospect Vernadskogo 7', 'Vernadskogo@yandex.ru', 'https://Vernadskogo.ru', '79256223089');
GO

CREATE TRIGGER PolyclinicaVIEWUpdate ON PolyclinicaVIEW
INSTEAD OF Update
AS
BEGIN
	IF UPDATE(PolyclinicID)
	BEGIN
		RAISERROR('Операция обновления PolyclinicID у Polyclinica невозможна и была отменена', 16, 1);
		ROLLBACK TRANSACTION
	END
	ELSE
	BEGIN
		UPDATE lab13_first.dbo.Polyclinica SET LicenseNum = inserted.LicenseNum, BranchNum = inserted.BranchNum, AddressMin = inserted.AddressMin FROM inserted
		WHERE lab13_first.dbo.Polyclinica.PolyclinicID = inserted.PolyclinicID
		UPDATE lab13_second.dbo.Polyclinica SET Email = inserted.Email, WebsiteLink = inserted.WebsiteLink, PhoneNum = inserted.PhoneNum FROM inserted
		WHERE lab13_second.dbo.Polyclinica.PolyclinicID = inserted.PolyclinicID
	END
END
GO

UPDATE PolyclinicaVIEW SET AddressMin = 'Kolomenskaya 20' WHERE PolyclinicID = 9;
UPDATE PolyclinicaVIEW SET AddressMin = 'under repair', WebsiteLink = 'https://mos.ru' WHERE PolyclinicID BETWEEN 4 and 6;
GO



CREATE TRIGGER PolyclinicaVIEWDelete ON PolyclinicaVIEW
INSTEAD OF delete
AS
	DELETE FROM lab13_first.dbo.Polyclinica WHERE PolyclinicID in (SELECT PolyclinicID FROM deleted)
	DELETE FROM lab13_second.dbo.Polyclinica WHERE PolyclinicID in (SELECT PolyclinicID FROM deleted)
GO

DELETE FROM PolyclinicaVIEW WHERE  PolyclinicID < 3;
DELETE FROM PolyclinicaVIEW WHERE PolyclinicID = 10;
GO

SELECT * FROM lab13_first.dbo.Polyclinica
SELECT * FROM lab13_second.dbo.Polyclinica
SELECT * FROM PolyclinicaVIEW
GO


--- поправить чтобы работало
--- При выполнении будет выведена ошибка
--select * from PolyclinicaVIEW 
--update PolyclinicaVIEW set PolyclinicID = PolyclinicID+3 
--select * from PolyclinicaVIEW 
--GO

USE lab13_first;
DROP TABLE Polyclinica
GO

USE lab13_second;
DROP TABLE Polyclinica
DROP TRIGGER PolyclinicaVIEWInsert
DROP TRIGGER PolyclinicaVIEWUpdate
DROP TRIGGER PolyclinicaVIEWDelete
DROP VIEW PolyclinicaVIEW
GO