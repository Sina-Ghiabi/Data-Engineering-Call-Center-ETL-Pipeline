import xlsxwriter

OUTPUT_FILE = "Analyze_Data.xlsx"


def export(tree):
    workbook = xlsxwriter.Workbook(OUTPUT_FILE)
    sheet = workbook.add_worksheet()
    columns = tree["columns"]
    items = tree.get_children()

    for column_index, column_name in enumerate(columns):
        sheet.write(0, column_index, column_name)

    for row_index, item_id in enumerate(items, start=1):
        values = tree.item(item_id)["values"]
        for column_index in range(len(columns)):
            sheet.write(row_index, column_index, values[column_index])

    workbook.close()
