from Control import DB_Connection

#Fill The Dropdowns With Data In Dropdown Tables
def Get_Dropdown_Value(self):
    Cursor = DB_Connection.Connect.cursor()
    Cursor.execute('SELECT ' + self.Dropdown + ' FROM Dropdown_' + self.Dropdown)
    Result = Cursor.fetchall()
    DB_Connection.Connect.commit()
    List = []
    for Index in Result:
        List.append(" | ".join(Index))
    return List