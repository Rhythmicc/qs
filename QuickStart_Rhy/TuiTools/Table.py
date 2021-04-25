"""
Generate Various Table
"""


def qs_default_table(headers: list, title: str = ''):
    from rich.table import Table
    from rich.box import SIMPLE_HEAVY

    res_table = Table(show_edge=False, row_styles=['none', 'dim'], box=SIMPLE_HEAVY, title=('[bold underline]' + title if title else ''))
    for i in headers:
        if isinstance(i, str):
            res_table.add_column(i, justify='center')
        elif isinstance(i, dict):
            res_table.add_column(**i)
        else:
            res_table.add_column(*i)

    return res_table
