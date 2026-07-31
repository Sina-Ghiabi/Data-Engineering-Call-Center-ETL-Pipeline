from tkinter import filedialog

from Control import DB_Connection , ProgressBar_Module
from View import Frame_View , Main_View
import re

#Insert Data From Imported File To The Tables
def Insert_Database():
    Main_View.Tree_View.delete(*Main_View.Tree_View.get_children())
    Queries = []
    Index = 0

    # Open Specific File Path
    Frame_View.Window.filename = filedialog.askopenfilename(title="Select a File", filetypes=(('text files', 'txt'),))
    # Read Specific File
    Length = len(open(Frame_View.Window.filename, 'r').readlines())
    # Read Specific File
    with open(Frame_View.Window.filename, buffering=10000000) as Every_Line:

        #Create ProgressBar Using ProgressBar_Module
        ProgressBar = ProgressBar_Module.ProgressBar("خواندن اطلاعات ..." )
        ProgressBar.Create_ProgressBar()

        for Data in Every_Line:

            Column = re.split(',', Data)

            if Column[0][0] == "#":
                pass
            else:
                Queries.append(
                    "INSERT INTO [dbo].[Unique_Info](Date_And_Time, Caller_Number,	Caller_Channel,	Called_Number,	Called_Channel,	Ring_Time , Talk_Time,	Status,	Details) VALUES('" +
                    Column[1] + "','" + Column[2] + "','" + Column[3] + "','" + Column[4] + "','" + Column[5] + "','" +
                    Column[
                        6] + "','" +
                    Column[7] + "','" + Column[8] + "','" + Column[9] + "');")

                if Index % 100 == 0:
                    Query = "".join(Queries)
                    Cursor = DB_Connection.Connect.cursor()
                    Cursor.execute(Query)
                    DB_Connection.Connect.commit()
                    Queries.clear()

                    # Progress_Bar_Value In Main_View
                    ProgressBar.Calculate_ProgressBar(Index,Length)

                Index = Index + 1

                #This Query Deletes Duplicate Rows
                if Index == Length - 1:
                    Query = "".join(Queries)
                    Cursor.execute(Query)
                    DB_Connection.Connect.commit()
                    Queries.clear()
                    Cursor.execute(
                        'WITH CTE AS(SELECT Date_And_Time, Caller_Number, Caller_Channel, Called_Number, Called_Channel, Ring_Time, Talk_Time, Status, Details,RN=ROW_NUMBER() OVER(PARTITION BY Date_And_Time, Caller_Number, Caller_Channel, Called_Number, Called_Channel, Ring_Time, Talk_Time, Status, Details ORDER BY Date_And_Time, Caller_Number, Caller_Channel, Called_Number, Called_Channel, Ring_Time, Talk_Time, Status, Details) FROM Unique_Info) DELETE FROM CTE WHERE RN>1 ')
                    DB_Connection.Connect.commit()

    ProgressBar.Destroy_ProgressBar()
