-- «адача: 1 —оздать базу данных (CREATE DATABASEЕ, определение настроек размеров файлов).
-- 2 —оздать произвольную таблицу (CREATE TABLEЕ).
-- 3 ƒобавить файловую группу и файл данных (ALTER DATABASEЕ).
-- 4 —делать созданную файловую группу файловой группой по умолчанию.
-- 5 —оздать еще одну произвольную таблицу.
-- 6 ”далить созданную вручную файловую группу.
-- 7 —оздать схему, переместить в нее одну из таблиц, удалить схему.


-- 1. —оздать базу данных
use master
GO

IF (
	SELECT name
	FROM sys.databases
	WHERE name = N'lab_5_Nikitin'
) IS NOT NULL
DROP DATABASE lab_5_Nikitin
GO

CREATE DATABASE [lab_5_Nikitin]
	ON ( NAME = lab_5_Nikitin_dat, FILENAME = 'D:\DBlabs\lab_5_Nikitindat.mdf', SIZE = 10, MAXSIZE = UNLIMITED, FILEGROWTH = 5% )
	LOG ON ( NAME = lab_5_Nikitin_log, FILENAME = 'D:\DBlabs\lab_5_Nikitinlog.ldf', SIZE = 5MB, MAXSIZE = 25MB, FILEGROWTH = 5MB );
GO


-- 2. —оздать произвольную таблицу (CREATE TABLEЕ).
USE lab_5_Nikitin
GO


IF OBJECT_ID(N'Ministry') is NOT NULL
    DROP TABLE Ministry;
GO

CREATE TABLE Ministry
(
    id INT PRIMARY KEY,
    location NVARCHAR(50) NOT NULL,
    phoneNum NVARCHAR(11) NOT NULL,
	addressMin NVARCHAR(200) NULL,
    email NVARCHAR(255) NOT NULL,
    websiteLink CHAR(2048) NOT NULL,
);
GO

SELECT * FROM Ministry;
GO


-- 3. ƒобавить файловую группу и файл данных (ALTER DATABASEЕ).
ALTER DATABASE lab_5_Nikitin
    ADD FILEGROUP LargeFileGroup;  
GO

ALTER DATABASE lab_5_Nikitin
    ADD FILE(
        NAME = lab_5_Nikitin_LargeData,  
        FILENAME = 'D:\DBlabs\lab_5_Nikitindat.ndf',
        SIZE = 5MB,
        MAXSIZE = 25MB,
        FILEGROWTH = 5% 
    )
TO FILEGROUP LargeFileGroup
GO

-- 4. —делать созданную файловую группу файловой группой по умолчанию.
ALTER DATABASE lab_5_Nikitin
    MODIFY FILEGROUP LargeFileGroup DEFAULT;
GO

-- 5. —оздать еще одну произвольную таблицу.
IF OBJECT_ID(N'Polyclinic') is NOT NULL
    DROP TABLE Polyclinic;
GO

CREATE TABLE Polyclinic
(
    id INT PRIMARY KEY,
    licenseNum INT NOT NULL,
    branchNum INT NOT NULL,
	addressMin NVARCHAR(200) NULL,
    email NVARCHAR(255) NOT NULL,
    websiteLink CHAR(2048) NOT NULL,
);
GO

SELECT * FROM Polyclinic;
GO


-- 6. ”далить созданную вручную файловую группу.
ALTER DATABASE lab_5_Nikitin
    MODIFY FILEGROUP [primary] DEFAULT;
GO

DROP TABLE Polyclinic;
GO

ALTER DATABASE lab_5_Nikitin
    REMOVE FILE lab_5_Nikitin_LargeData;
GO

ALTER DATABASE lab_5_Nikitin
    REMOVE FILEGROUP LargeFileGroup;
GO



-- 7. —оздать схему, переместить в нее одну из таблиц, удалить схему.
IF SCHEMA_ID(N'MinystryScheme') is NOT NULL
    DROP SCHEMA MinystryScheme;
GO

CREATE SCHEMA MinystryScheme;
GO

ALTER SCHEMA MinystryScheme
    TRANSFER Ministry;
GO

IF OBJECT_ID(N'MinystryScheme.Ministry') is NOT NULL
    DROP TABLE MinystryScheme.Ministry;
GO

DROP SCHEMA MinystryScheme;
GO