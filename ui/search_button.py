from database import db_connection
from ui.query_builder import build_search_query


def _period_values(period_entries):
    return {
        field_name: (entry_from.get(), entry_to.get())
        for field_name, (entry_from, entry_to) in period_entries.items()
    }


def _populate_tree(tree, query, params) -> int:
    tree.delete(*tree.get_children())

    connection = db_connection.get_connection()
    cursor = connection.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    connection.commit()

    for index, row in enumerate(rows):
        tag = "even" if index % 2 == 0 else "odd"
        tree.insert("", "end", values=tuple(row[1:]), tags=(tag,))

    return len(rows)


def search(tree, dropdown_selections, period_entries, status_bar) -> None:
    query, params = build_search_query(dropdown_selections, _period_values(period_entries))
    count = _populate_tree(tree, query, params)
    dropdown_selections.clear()
    status_bar.finish_progress(f"Report generated successfully — {count} record(s) found.")


def load_all(tree) -> int:
    return _populate_tree(tree, "SELECT * FROM Separated_Info", [])
