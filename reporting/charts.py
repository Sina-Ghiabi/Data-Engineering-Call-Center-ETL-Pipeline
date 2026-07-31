from reporting.pie_chart import PieChart


def _show_all(number):
    chart = PieChart(number)
    chart.all_calls()
    chart.status_breakdown()
    chart.io_breakdown()
    chart.input_calls()
    chart.output_calls()


def show_details(caller_number="", called_number=""):
    if caller_number:
        _show_all(caller_number)
    if called_number:
        _show_all(called_number)
