IF DB_ID('Users') IS NULL
BEGIN
    CREATE DATABASE Users;
END
GO

USE Users;
GO

IF OBJECT_ID('dbo.Unique_Info', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Unique_Info (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        Date_And_Time NVARCHAR(50) NOT NULL,
        Caller_Number NVARCHAR(50) NOT NULL,
        Caller_Channel NVARCHAR(50) NOT NULL,
        Called_Number NVARCHAR(50) NOT NULL,
        Called_Channel NVARCHAR(50) NOT NULL,
        Ring_Time NVARCHAR(20) NOT NULL,
        Talk_Time NVARCHAR(20) NOT NULL,
        Status NVARCHAR(20) NOT NULL,
        Details NVARCHAR(200) NOT NULL
    );
END
GO

IF OBJECT_ID('dbo.Separated_Info', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Separated_Info (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        Date NVARCHAR(20) NOT NULL,
        Year NVARCHAR(10) NOT NULL,
        Month NVARCHAR(10) NOT NULL,
        Day NVARCHAR(10) NOT NULL,
        Time NVARCHAR(20) NOT NULL,
        IO_Caller_Number NVARCHAR(50) NOT NULL,
        IO_Caller_Number_Section NVARCHAR(20) NOT NULL,
        Caller_Number NVARCHAR(50) NOT NULL,
        Caller_Channel_Code NVARCHAR(20) NOT NULL,
        Caller_Channel NVARCHAR(50) NOT NULL,
        IO_Called_Number NVARCHAR(50) NOT NULL,
        IO_Called_Number_Section NVARCHAR(20) NOT NULL,
        Called_Number NVARCHAR(50) NOT NULL,
        Called_Channel_Code NVARCHAR(20) NOT NULL,
        Called_Channel NVARCHAR(50) NOT NULL,
        Ring_Time NVARCHAR(20) NOT NULL,
        Talk_Time NVARCHAR(20) NOT NULL,
        Status NVARCHAR(20) NOT NULL,
        Details NVARCHAR(200) NOT NULL
    );
END
GO

IF OBJECT_ID('dbo.Dropdown_IO_Caller_Section', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dropdown_IO_Caller_Section (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        IO_Caller_Section NVARCHAR(20) NOT NULL
    );
END
GO

IF OBJECT_ID('dbo.Dropdown_IO_Called_Section', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dropdown_IO_Called_Section (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        IO_Called_Section NVARCHAR(20) NOT NULL
    );
END
GO

IF OBJECT_ID('dbo.Dropdown_Status', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dropdown_Status (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        Status NVARCHAR(20) NOT NULL
    );
END
GO

IF OBJECT_ID('dbo.Dropdown_Caller_Channel_Code', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dropdown_Caller_Channel_Code (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        Caller_Channel_Code NVARCHAR(20) NOT NULL
    );
END
GO

IF OBJECT_ID('dbo.Dropdown_Called_Channel_Code', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dropdown_Called_Channel_Code (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        Called_Channel_Code NVARCHAR(20) NOT NULL
    );
END
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Dropdown_IO_Caller_Section)
BEGIN
    INSERT INTO dbo.Dropdown_IO_Caller_Section (IO_Caller_Section)
    VALUES ('All'), ('External'), ('Brokerage'), ('Box'), ('Invalid');
END
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Dropdown_IO_Called_Section)
BEGIN
    INSERT INTO dbo.Dropdown_IO_Called_Section (IO_Called_Section)
    VALUES ('All'), ('External'), ('Brokerage'), ('Box'), ('Invalid');
END
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Dropdown_Status)
BEGIN
    INSERT INTO dbo.Dropdown_Status (Status)
    VALUES ('All'), ('answered'), ('busy'), ('No answer'), ('Failed');
END
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Dropdown_Caller_Channel_Code)
BEGIN
    INSERT INTO dbo.Dropdown_Caller_Channel_Code (Caller_Channel_Code) VALUES ('All');
END
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Dropdown_Called_Channel_Code)
BEGIN
    INSERT INTO dbo.Dropdown_Called_Channel_Code (Called_Channel_Code) VALUES ('All');
END
GO

-- Batch/lineage metadata for "Export to Table". One row per export click;
-- the app also creates this table lazily on first export, so running this
-- script is optional, not required, for that feature to work.
IF OBJECT_ID('dbo.Export_Batches', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Export_Batches (
        BatchID INT IDENTITY(1,1) PRIMARY KEY,
        TableName NVARCHAR(128) NOT NULL,
        ExportedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        FilterCriteria NVARCHAR(MAX) NOT NULL,
        RecordCount INT NOT NULL
    );
END
GO
