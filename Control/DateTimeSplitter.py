import queue
import re

Date_And_Time_Queue = queue.Queue()
Caller_Queue = queue.Queue()
Called_Queue = queue.Queue()

#Splits Date To Year Month Day Time And Returns It Using Queue
def Splitter(Data):
    try:
        Date_And_Time = re.split(' ', Data)
        Separated_Date = re.split('/', Date_And_Time[0])

        Output_Date_And_Time = [Date_And_Time[0], Separated_Date[0], Separated_Date[1], Separated_Date[2],
                                Date_And_Time[1]]
        Date_And_Time_Queue.put(Output_Date_And_Time)
    except:
        Output_Date_And_Time = ["None", "None", "None", "None", "None"]
        Date_And_Time_Queue.put(Output_Date_And_Time)
