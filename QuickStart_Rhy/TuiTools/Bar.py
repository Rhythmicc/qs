# coding=utf-8
"""
柱状图

histogram & Bar
"""


def DataTransformBar(has_size_info: bool = True):
    """
    创建一个数据传输进度条

    Create a data transfer progress bar

    :param has_size_info: 是否有总任务量
    :return: rich.progress.Progress
    """
    from rich.progress import (
        Progress,
        TextColumn,
        BarColumn,
        DownloadColumn,
        TransferSpeedColumn,
        TimeRemainingColumn,
    )
    from .. import qs_default_console

    if has_size_info:
        return Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
            console=qs_default_console,
        )
    else:
        from .. import user_lang

        return Progress(
            TextColumn(
                "[bold blue]{task.fields[filename]} [red]"
                + ("Unknow size" if user_lang != "zh" else "未知大小"),
                justify="right",
            ),
            BarColumn(bar_width=None),
            DownloadColumn(),
            console=qs_default_console,
        )


def NormalProgressBar(task_name, total):
    from .. import qs_default_console
    from rich.progress import Progress

    progress = Progress()
    task_id = progress.add_task(task_name, total=total, console=qs_default_console)
    return progress, task_id
