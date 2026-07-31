import xlsxwriter
from View import Main_View

#Export Data From Treeview To Excel
def Export_Exel():
    Exel = xlsxwriter.Workbook("Analyze_Data.xlsx")
    Export_Exel = Exel.add_worksheet()
    Treeview_Data = Main_View.Tree_View.get_children()

    for Index in range(0, len(Main_View.Tree_View['columns'])):
        Export_Exel.write(0, Index, Main_View.Tree_View['columns'][Index])

    for Index1 in range(1, len(Main_View.Tree_View.get_children())):
        for Index2 in range(0, 19):
            Export_Exel.write(Index1, Index2, Main_View.Tree_View.item(Treeview_Data[Index1])["values"][Index2])
    Exel.close()
