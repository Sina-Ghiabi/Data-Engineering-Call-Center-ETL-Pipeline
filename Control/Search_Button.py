from tkinter import *

from Control import Dropdown_Module , DB_Connection
from View import Frame_View , Main_View

def Click():
    Main_View.Tree_View.Tree_View.delete(*Main_View.Tree_View.Tree_View.get_children())

    Selected_Dropdowns = Dropdown_Module.Dictionary
    Query = "SELECT * FROM Separated_Info WHERE ID LIKE '%%'"

    if "IO_Caller_Section" in Selected_Dropdowns:
        if Selected_Dropdowns['IO_Caller_Section'] == 'انتخاب همه':
            pass
        else:
            Query = Query + " AND IO_Caller_Number_Section = N'" + Selected_Dropdowns['IO_Caller_Section'] + "'"

    if "Caller_Channel_Code" in Selected_Dropdowns:
        if Selected_Dropdowns['Caller_Channel_Code'] == 'انتخاب همه':
            pass
        else:
            Query = Query + " AND Caller_Channel_Code =  '" + Selected_Dropdowns['Caller_Channel_Code'] + "'"

    if "IO_Called_Section" in Selected_Dropdowns:
        if Selected_Dropdowns['IO_Called_Section'] == 'انتخاب همه':
            pass
        else:
            Query = Query + " AND IO_Called_Number_Section = N'" + Selected_Dropdowns['IO_Called_Section'] + "'"

    if "Called_Channel_Code" in Selected_Dropdowns:
        if Selected_Dropdowns['Called_Channel_Code'] == 'انتخاب همه':
            pass
        else:
            Query = Query + " AND Called_Channel_Code = '" + Selected_Dropdowns["Called_Channel_Code"] + "'"

    if "Status" in Selected_Dropdowns:
        if Selected_Dropdowns['Status'] == 'انتخاب همه':
            pass
        else:
            Query = Query + " AND Status = '" + Selected_Dropdowns["Status"] + "'"

    # Ring Time Textboxes
    if Main_View.Ring_Time_Textbox1.get() != "" and Main_View.Ring_Time_Textbox2.get() != "":
        Query = Query + " AND '" + Main_View.Ring_Time_Textbox1.get() + "' <= Ring_Time AND Ring_Time <= '" + Main_View.Ring_Time_Textbox2.get() + "'"

    if Main_View.Ring_Time_Textbox1.get() != "" and Main_View.Ring_Time_Textbox2.get() == "":
        Query = Query + " AND '" + Main_View.Ring_Time_Textbox1.get() + "' <= Ring_Time "

    if Main_View.Ring_Time_Textbox1.get() == "" and Main_View.Ring_Time_Textbox2.get() != "":
        Query = Query + " AND Ring_Time <= '" + Main_View.Ring_Time_Textbox2.get() + "'"

    # Talk Time Textboxes
    if Main_View.Talk_Time_Textbox1.get() != "" and Main_View.Talk_Time_Textbox2.get() != "":
        Query = Query + " AND '" + Main_View.Talk_Time_Textbox1.get() + "' <= Talk_Time AND Talk_Time <= '" + Main_View.Talk_Time_Textbox2.get() + "'"

    if Main_View.Talk_Time_Textbox1.get() != "" and Main_View.Talk_Time_Textbox2.get() == "":
        Query = Query + " AND '" + Main_View.Talk_Time_Textbox1.get() + "' <= Talk_Time "

    if Main_View.Talk_Time_Textbox1.get() == "" and Main_View.Talk_Time_Textbox2.get() != "":
        Query = Query + " AND Talk_Time <= '" + Main_View.Talk_Time_Textbox2.get() + "'"

    # Date Textboxes
    if Main_View.Date_Textbox1.get() != "" and Main_View.Date_Textbox2.get() != "":
        Query = Query + " AND '" + Main_View.Date_Textbox1.get() + "' <= Date AND Date <= '" + Main_View.Date_Textbox2.get() + "'"

    if Main_View.Date_Textbox1.get() != "" and Main_View.Date_Textbox2.get() == "":
        Query = Query + " AND '" + Main_View.Date_Textbox1.get() + "' <= Date "

    if Main_View.Date_Textbox1.get() == "" and Main_View.Date_Textbox2.get() != "":
        Query = Query + " AND Date <= '" + Main_View.Date_Textbox2.get() + "'"

    # Time Textboxes
    if Main_View.Time_Textbox1.get() != "" and Main_View.Time_Textbox2.get() != "":
        Query = Query + " AND '" + Main_View.Time_Textbox1.get() + "' <= Time AND Time <= '" + Main_View.Time_Textbox2.get() + "'"

    if Main_View.Time_Textbox1.get() != "" and Main_View.Time_Textbox2.get() == "":
        Query = Query + " AND '" + Main_View.Time_Textbox1.get() + "' <= Time "

    if Main_View.Time_Textbox1.get() == "" and Main_View.Time_Textbox2.get() != "":
        Query = Query + " AND Time <= '" + Main_View.Time_Textbox2.get() + "'"

    Cursor = DB_Connection.Connect.cursor()
    Cursor.execute(Query)
    Result = Cursor.fetchall()
    DB_Connection.Connect.commit()

    # if Main_View.Checkbox_Variable.get() == 1:
    #     Holidays_Query = "SELECT * FROM Holidays WHERE '" + Main_View.Date_Textbox1.get() + "' <= Date AND Date <= '" + Main_View.Date_Textbox2.get() + "'"
    #
    #     Holidays = []
    #     Cursor = DB_Connection.Connect.cursor()
    #     Cursor.execute(Holidays_Query)
    #     Holidays_Result = Cursor.fetchall()
    #     DB_Connection.Connect.commit()
    #     # Get Days Off From Databse And Save It In Holidays Array
    #     for Results in Holidays_Result:
    #         Holidays.append(Results[1])
    #
    #     for Index in range(0, 19):
    #         Main_View.Tree_View.column(str(Index), anchor=W, width=75, stretch=NO)
    #         Main_View.Tree_View.heading("#0", text="ID", anchor=W)
    #         Main_View.Tree_View.heading(str(Index), text=Main_View.Tree_View["columns"][Index], anchor=W)
    #
    #     for Index in range(0, len(Result)):
    #         if Result[Index][1] in Holidays:
    #             print(Result[Index])
    #             continue
    #         else:
    #             Main_View.Tree_View.insert('', 'end', 'Item' + str(Index), text=Index, values=(
    #                 Result[Index][1], Result[Index][2], Result[Index][3], Result[Index][4], Result[Index][5],
    #                 Result[Index][6],
    #                 Result[Index][7], Result[Index][8], Result[Index][9], Result[Index][10], Result[Index][11],
    #                 Result[Index][12], Result[Index][13], Result[Index][14], Result[Index][15], Result[Index][16],
    #                 Result[Index][17], Result[Index][18], Result[Index][19]))
    #
    # if Main_View.Checkbox_Variable.get() == 0:
    #     for Index in range(0, 19):
    #         Main_View.Tree_View.column(str(Index), anchor=W, width=75, stretch=NO)
    #         Main_View.Tree_View.heading("#0", text="ID", anchor=W)
    #         Main_View.Tree_View.heading(str(Index), text=Main_View.Tree_View["columns"][Index], anchor=W)
    #
    #     for Index in range(0, len(Result)):
    #         Main_View.Tree_View.insert('', 'end', 'Item' + str(Index), text=Index, values=(
    #             Result[Index][1], Result[Index][2], Result[Index][3], Result[Index][4], Result[Index][5],
    #             Result[Index][6],
    #             Result[Index][7], Result[Index][8], Result[Index][9], Result[Index][10], Result[Index][11],
    #             Result[Index][12], Result[Index][13], Result[Index][14], Result[Index][15], Result[Index][16],
    #             Result[Index][17], Result[Index][18], Result[Index][19]))
    #

    Succeed_Label = Label(Frame_View.Window, text='تهيه گزارش با موفقيت انجام شد')
    Succeed_Label.place(x=425, y=550)
    Dropdown_Module.Dictionary.clear()