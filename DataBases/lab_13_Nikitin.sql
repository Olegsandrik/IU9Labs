USE master;
GO

IF DB_ID('lab13_first') IS NOT NULL
DROP DATABASE lab13_first;
GO

IF DB_ID('lab13_second') IS NOT NULL
DROP DATABASE lab13_second;
GO

CREATE DATABASE lab13_first;
CREATE DATABASE lab13_second;
GO

USE lab13_first;

CREATE TABLE Polyclinic
(
    PolyclinicID INT PRIMARY KEY CHECK (PolyclinicID BETWEEN 1 AND 5),
    LicenseNum INT NOT NULL,
    BranchNum INT NOT NULL,
	AddressMin NVARCHAR(200) NULL,
    Email NVARCHAR(255) NOT NULL,
    WebsiteLink CHAR(2048) NOT NULL,
	PhoneNum NVARCHAR(11) NOT NULL
);
GO

USE lab13_second;

CREATE TABLE Polyclinic
(
    PolyclinicID INT PRIMARY KEY CHECK (PolyclinicID BETWEEN 6 AND 10000),
    LicenseNum INT NOT NULL,
    BranchNum INT NOT NULL,
	AddressMin NVARCHAR(200) NULL,
    Email NVARCHAR(255) NOT NULL,
    WebsiteLink CHAR(2048) NOT NULL,
	PhoneNum NVARCHAR(11) NOT NULL
);
GO



CREATE VIEW PolyclinicVIEW AS
	SELECT * FROM lab13_first.dbo.Polyclinic
	UNION ALL
	SELECT * FROM lab13_second.dbo.Polyclinic
GO


INSERT INTO PolyclinicVIEW(PolyclinicID, LicenseNum, BranchNum, AddressMin, Email, WebsiteLink, PhoneNum)
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


SELECT * FROM PolyclinicVIEW;
SELECT * FROM lab13_first.dbo.Polyclinic
SELECT * FROM lab13_second.dbo.Polyclinic
GO


UPDATE PolyclinicVIEW SET PolyclinicID = 11 WHERE PolyclinicID = 2;
SELECT * FROM PolyclinicVIEW;

SELECT * FROM lab13_first.dbo.Polyclinic
SELECT * FROM lab13_second.dbo.Polyclinic
GO

DELETE PolyclinicVIEW WHERE PolyclinicID > 8;
SELECT * FROM PolyclinicVIEW;

SELECT * FROM lab13_first.dbo.Polyclinic
SELECT * FROM lab13_second.dbo.Polyclinic
GO