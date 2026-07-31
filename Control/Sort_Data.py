from Control import DB_Connection , ProgressBar_Module , DateTimeSplitter

import queue
import re

Date_And_Time_Queue = queue.Queue()
Caller_Queue = queue.Queue()
Called_Queue = queue.Queue()

def Sort_Database():

    #Define DateTime Input & Output Arrays
    DateTime_Input = []
    Date = []
    Year = []
    Month = []
    Day = []
    Time = []

    #Define Caller & Called Input Arrays
    Caller_Input = []
    Called_Input = []

    #Define Caller & Called Output Arrays
    Caller_Number_Output = []
    Called_Number_Output = []

    #Define Caller & Called Section Arrays
    Caller_Section_Output = []
    Called_Section_Output = []

    #Define Query Array
    Queries = []

    #Get DateTime From Queue & Separate It
    DateTime_Output = Date_And_Time_Queue.get()
    Date.append(DateTime_Output[0])
    Year.append(DateTime_Output[1])
    Month.append(DateTime_Output[2])
    Day.append(DateTime_Output[3])
    Time.append(DateTime_Output[4])

    #Get Caller Number & Section From Queue
    Caller_Output = Caller_Queue.get()
    Caller_Number_Output.append(Caller_Output[0][1])
    Caller_Section_Output.append(Caller_Output[0][0])

    #Get Called Number & Section From Queue
    Called_Output = Called_Queue.get()
    Called_Number_Output.append(Called_Output[0][1])
    Called_Section_Output.append(Called_Output[0][0])

    #Get Number Of Rows & Use It For ProgressBar 
    Cursor = DB_Connection.Connect.cursor()
    Cursor.execute('select count(ID) from Unique_Info ')
    Number = Cursor.fetchall()
    Length = Number[0][0]

    #Fetching Data From Unique_Info & Queue To Manage & Insert Them To Separated_Info
    Cursor.execute('SELECT * FROM Unique_Info')
    Result = Cursor.fetchall()

    ProgressBar = ProgressBar_Module.ProgressBar("پردازش اطلاعات ...")

    for Index in range(0, len(Result)):
        DateTime_Input.append(Result[Index][1])
    for Row in Result:
        Caller_Input.append([Row[2]])
    for Row in Result:
        Called_Input.append([Row[4]])

    #Split DateTime To Date , Year , Month , Day Time Using DateTime Splitter And Return Data Using Queue
    DateTimeSplitter.Splitter(DateTime_Input)
    DateTime_Queue = Date_And_Time_Queue.get()
    Date.append(DateTime_Queue[0])
    Year.append(DateTime_Queue[1])
    Month.append(DateTime_Queue[2])
    Day.append(DateTime_Queue[3])
    Time.append(DateTime_Queue[4])

    for Index in range(0, len(Result)):

        Caller_Number_Query = Caller_Number_Output[Index]
        Caller_Section_Query = Caller_Section_Output[Index]
        Called_Number_Query = Called_Number_Output[Index]
        Called_Section_Query = Called_Section_Output[Index]

        Query_Date = Date[Index]
        Query_Year = Year[Index]
        Query_Month = Month[Index]
        Query_Day = Day[Index]
        Query_Time = Time[Index]

        if Index >= len(Result):
            print("Finished")
            break

        try:
            Caller_Channel = re.split(':', Result[Index][3])
            Caller_Channel_Code = Caller_Channel[0]
            Caller_Channel_Number = Caller_Channel[1]

        except:
            Caller_Channel_Code = "None"
            Caller_Channel_Number = "None"

        try:
            if ":" not in Result[Index][5]:
                Called_Channel_Code = "-"
                Called_Channel_Number = "-"
            else:
                Called_Channel = re.split(':', Result[Index][5])
                Called_Channel_Code = Called_Channel[0]
                Called_Channel_Number = Called_Channel[1]
        except:
            Called_Channel_Code = "None"
            Called_Channel_Number = "None"

        #Insert Into Separated_Info
        Queries.append(
            "INSERT INTO [dbo].[Separated_Info](Date,Year,Month,Day,Time, IO_Caller_Number,IO_Caller_Number_Section,Caller_Number,Caller_Channel_Code,Caller_Channel,IO_Called_Number,IO_Called_Number_Section ,Called_Number, Called_Channel_Code,Called_Channel, Ring_Time, Talk_Time, Status, Details) VALUES('" +
            Query_Date + "','" + Query_Year + "','" + Query_Month + "','" + Query_Day + "','" + Query_Time + "','" +
            Caller_Number_Query + "','" +
            Caller_Section_Query + "','" + Result[Index][
                2] + "','" + Caller_Channel_Code + "','" + Caller_Channel_Number + "','" + Called_Number_Query + "','" + Called_Section_Query + "','" +
            Result[Index][4] + "','" + Called_Channel_Code + "','" + Called_Channel_Number + "','" + Result[Index][
                6] + "','" + Result[Index][7] + "','" + Result[Index][8] + "','" + Result[Index][9] + "');")

        #ProgressBar For Inserting Into Separated_Info
        if Index % 100 == 0:
            Query = "".join(Queries)
            Cursor.execute(Query)
            Queries.clear()
            # Separate_Info Progress_Bar
            ProgressBar.Calculate_ProgressBar(Index,Length)
            DB_Connection.Connect.commit()

        if Index == Length - 1:
            Query = "".join(Queries)
            Cursor.execute(Query)
            DB_Connection.Connect.commit()
            Queries.clear()
            Cursor.execute(
                'WITH CTE AS(SELECT Date,Year,Month,Day,Time, IO_Caller_Number,IO_Caller_Number_Section,Caller_Number,Caller_Channel_Code,Caller_Channel,IO_Called_Number,IO_Called_Number_Section ,Called_Number, Called_Channel_Code,Called_Channel, Ring_Time, Talk_Time, Status, Details,RN=ROW_NUMBER() OVER(PARTITION BY Date,Year,Month,Day,Time, IO_Caller_Number,IO_Caller_Number_Section,Caller_Number,Caller_Channel_Code,Caller_Channel,IO_Called_Number,IO_Called_Number_Section ,Called_Number, Called_Channel_Code,Called_Channel, Ring_Time, Talk_Time, Status, Details ORDER BY Date,Year,Month,Day,Time, IO_Caller_Number,IO_Caller_Number_Section,Caller_Number,Caller_Channel_Code,Caller_Channel,IO_Called_Number,IO_Called_Number_Section ,Called_Number, Called_Channel_Code,Called_Channel, Ring_Time, Talk_Time, Status, Details) FROM Separated_Info) DELETE FROM CTE WHERE RN>1 ')
            DB_Connection.Connect.commit()

    ProgressBar.Destroy_ProgressBar()
