import matplotlib.pyplot as plt

from database import db_connection


class PieChart:
    def __init__(self, number):
        self.number = number

    @staticmethod
    def _show(labels, values):
        _figure, axes = plt.subplots()
        axes.pie(values, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90)
        axes.axis("equal")
        plt.show()

    def _count(self, cursor, where_clause, params):
        cursor.execute(f"SELECT COUNT(ID) FROM Separated_Info WHERE {where_clause}", params)
        return cursor.fetchone()[0]

    def all_calls(self):
        cursor = db_connection.connection.cursor()
        total = self._count(cursor, "1 = 1", ())
        user_total = self._count(cursor, "Caller_Number = ?", (self.number,))
        db_connection.connection.commit()
        self._show(["All Calls", "User Calls"], [total, user_total])

    def input_calls(self):
        cursor = db_connection.connection.cursor()
        total = self._count(
            cursor,
            "IO_Called_Number_Section = 'Box' OR IO_Called_Number_Section = 'Brokerage'",
            (),
        )
        user_total = self._count(
            cursor,
            "Called_Number = ? AND (IO_Called_Number_Section = 'Box' OR IO_Called_Number_Section = 'Brokerage')",
            (self.number,),
        )
        self._show(["All Input Calls", "User Input Calls"], [total, user_total])

    def output_calls(self):
        cursor = db_connection.connection.cursor()
        total = self._count(cursor, "IO_Called_Number_Section = 'External'", ())
        user_total = self._count(
            cursor,
            "Called_Number = ? AND IO_Caller_Number_Section = 'External'",
            (self.number,),
        )
        self._show(["All Output Calls", "User Output Calls"], [total, user_total])

    def status_breakdown(self):
        cursor = db_connection.connection.cursor()
        statuses = ["answered", "busy", "No answer", "Failed"]
        values = [self._count(cursor, "Caller_Number = ? AND Status = ?", (self.number, status)) for status in statuses]
        db_connection.connection.commit()
        self._show(["Answered", "Busy", "No Answer", "Failed"], values)

    def io_breakdown(self):
        cursor = db_connection.connection.cursor()
        input_calls = self._count(
            cursor,
            "Called_Number = ? AND (IO_Caller_Number_Section = 'Brokerage' OR IO_Caller_Number_Section = 'Box')",
            (self.number,),
        )
        output_calls = self._count(
            cursor,
            "Called_Number = ? AND IO_Caller_Number_Section = 'External'",
            (self.number,),
        )
        self._show(["Input Calls", "Output Calls"], [input_calls, output_calls])
