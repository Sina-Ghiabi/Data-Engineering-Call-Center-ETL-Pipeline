USE Users;
GO

-- Run this after importing data, so the channel-code filters offer the
-- codes that actually showed up in Separated_Info (they come from the
-- raw call records, so there is no fixed list to seed ahead of time).

INSERT INTO dbo.Dropdown_Caller_Channel_Code (Caller_Channel_Code)
SELECT DISTINCT s.Caller_Channel_Code
FROM dbo.Separated_Info AS s
WHERE s.Caller_Channel_Code NOT IN (SELECT Caller_Channel_Code FROM dbo.Dropdown_Caller_Channel_Code);
GO

INSERT INTO dbo.Dropdown_Called_Channel_Code (Called_Channel_Code)
SELECT DISTINCT s.Called_Channel_Code
FROM dbo.Separated_Info AS s
WHERE s.Called_Channel_Code NOT IN (SELECT Called_Channel_Code FROM dbo.Dropdown_Called_Channel_Code);
GO
