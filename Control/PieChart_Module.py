from Control import DB_Connection
import matplotlib.pyplot as plt

#A Class To Create Multiple PieCharts
class Pie_Chart:
    def __init__(self, Number):
        self.Number = Number

    def Create_Pie_Chart(self, Labels, Values):
        Fig, Pie_Chart = plt.subplots()
        Pie_Chart.pie(Values, labels=Labels, autopct='%1.1f%%',
                      shadow=True, startangle=90)
        Pie_Chart.axis('equal')
        plt.show()

    def All_Users_Calls(self):
        Cursor = DB_Connection.Connect.cursor()
        Cursor.execute("SELECT Count(ID) FROM Separated_Info")
        All = Cursor.fetchall()[0][0]

        Cursor.execute("SELECT Count(ID) From Separated_Info WHERE Caller_Number='" + self.Number + "' ")
        User = Cursor.fetchall()[0][0]

        DB_Connection.Connect.commit()

        Labels = ['All Calls', 'Users Calls']
        Values = [All, User]

        Pie_Chart1 = Pie_Chart(self.Number)
        Pie_Chart1.Create_Pie_Chart(Labels, Values)

    def All_Users_Input_Calls(self):
        Cursor = DB_Connection.Connect.cursor()
        Cursor.execute(
            "SELECT Count(ID) FROM Separated_Info WHERE IO_Called_Number_Section='صندوق' or IO_Called_Number_Section ='کارگزاري'")
        All_Input_Calls = Cursor.fetchall()[0][0]

        Cursor.execute(
            "SELECT Count(ID) FROM Separated_Info WHERE Called_Number='110' and  IO_Called_Number_Section='صندوق' or IO_Called_Number_Section ='کارگزاري'")
        Specific_Input_Calls = Cursor.fetchall()[0][0]

        Labels = ['All Input Calls', 'Users Input Calls']
        Values = [All_Input_Calls, Specific_Input_Calls]

        Pie_Chart2 = Pie_Chart(self.Number)
        Pie_Chart2.Create_Pie_Chart(Labels, Values)

    def All_Users_Output_Calls(self):
        Cursor = DB_Connection.Connect.cursor()
        Cursor.execute("SELECT Count(ID) FROM Separated_Info WHERE IO_Called_Number_Section='خارجي'")
        All_Output_Calls = Cursor.fetchall()[0][0]

        Cursor.execute(
            "SELECT Count(ID) FROM Separated_Info WHERE Called_Number='" + self.Number + "' and IO_Caller_Number_Section='خارجي'")
        Specific_Output_Calls = Cursor.fetchall()[0][0]

        Labels = ['All Output Calls', 'Users Output Calls']
        Values = [All_Output_Calls, Specific_Output_Calls]

        Pie_Chart3 = Pie_Chart(self.Number)
        Pie_Chart3.Create_Pie_Chart(Labels, Values)

    def Analyze_Calls(self):
        Cursor = DB_Connection.Connect.cursor()

        Cursor.execute(
            "SELECT Count(ID) FROM Separated_Info WHERE Caller_Number='" + self.Number + "' and Status='answered'")
        Answered_Result = Cursor.fetchall()[0][0]

        Cursor.execute(
            "SELECT Count(ID) FROM Separated_Info WHERE Caller_Number='" + self.Number + "' and Status='busy'")
        Busy_Result = Cursor.fetchall()[0][0]

        Cursor.execute(
            "SELECT Count(ID) FROM Separated_Info WHERE Caller_Number='" + self.Number + "' and Status='No answer'")
        No_Answer_Result = Cursor.fetchall()[0][0]

        Cursor.execute(
            "SELECT Count(ID) FROM Separated_Info WHERE Caller_Number='" + self.Number + "' and Status='Failed'")
        Failed_Result = Cursor.fetchall()[0][0]

        DB_Connection.Connect.commit()

        Labels = ['Answered', 'Busy', 'No Answer', 'Failed']
        Values = [Answered_Result, Busy_Result, No_Answer_Result, Failed_Result]

        Pie_Chart4 = Pie_Chart(self.Number)
        Pie_Chart4.Create_Pie_Chart(Labels, Values)

    def Separate_IO_Calls(self):
        Cursor = DB_Connection.Connect.cursor()
        Cursor.execute(
            "SELECT Count(ID) FROM Separated_Info WHERE Called_Number='" + self.Number + "' and IO_Caller_Number_Section=N'کارگزاري' or IO_Caller_Number_Section=N'صندوق'")
        Input_Calls = Cursor.fetchall()[0][0]

        Cursor.execute(
            "SELECT Count(ID) FROM Separated_Info WHERE IO_Caller_Number_Section=N'خارجي' and  Called_Number='" + self.Number + "'")
        Output_Calls = Cursor.fetchall()[0][0]

        Labels = ['Input Calls', 'Output Calls']
        Values = [Input_Calls, Output_Calls]

        Pie_Chart5 = Pie_Chart(self.Number)
        Pie_Chart5.Create_Pie_Chart(Labels, Values)
