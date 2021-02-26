"""
Generate Various Table
"""


def qs_default_table(headers: list, title: str = ''):
    from rich.table import Table, Column
    from rich.box import SIMPLE

    return Table(
        *([Column(i, justify='center') for i in headers])
        , show_edge=False, row_styles=['none', 'dim'], box=SIMPLE, title=('[bold underline]' + title if title else '')
    )
