"""
Generate Various Table
"""


def qs_default_table(headers: list, title: str = "", without_headers: bool = False):
    """
    生成一个具有默认样式的表格

    header – 文本或可渲染的对象，用于表头。默认为 ""。

    footer – 文本或可渲染的对象，用于表尾。默认为 ""。

    header_style – 用于表头的样式，默认为 None。

    footer_style – 用于表尾的样式，默认为 None。

    style – 列单元格的样式，默认为None。

    justify – 单元格的对齐方式，默认为 "左"。

    vertical – 垂直排列, "top", "middle", 或 "bottom". 默认 "top".

    overflow – 溢出法: "crop", "fold", "ellipsis". 默认 "ellipsis".

    width – 栏目的预期宽度，以字符为单位，或无，以适应内容，默认 None.

    min_width – 列的最小宽度, 或 ``None`` 为无最低，默认 None.

    max_width – 列的最大宽度, 或 ``None`` 为无最大，默认 None.

    ratio – 列的灵活比率 (依赖 ``Table.expand`` 或 ``Table.width``)，默认 None.

    no_wrap – 设置为 "True"，可以禁用该列的包装。

    :param headers: list of str, dict or list
    :param title: title of the table
    :return:
    """
    from rich.table import Table
    from rich.box import SIMPLE_HEAVY

    res_table = Table(
        show_header=not without_headers,
        show_edge=False,
        row_styles=["none", "dim"],
        box=SIMPLE_HEAVY,
        title=title,
    )
    for i in headers:
        if isinstance(i, str):
            res_table.add_column(i, justify="center")
        elif isinstance(i, dict):
            res_table.add_column(**i)
        else:
            res_table.add_column(*i)

    return res_table
