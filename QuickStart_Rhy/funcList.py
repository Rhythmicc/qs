# coding=utf-8
"""
功能映射与菜单提示

Function mapping and menu prompt
"""
from . import qs_default_console, lang_detector
from .qsLesson import lesson

def menu_show(lines: list):
    from rich.table import Table, Column
    from rich.box import SIMPLE

    tb = Table(
        *(
            [
                Column("1", style="bold magenta", justify="left"),
                Column("2", style="bold yellow", justify="center"),
                Column("3", style="bold green", justify="right"),
            ]
        ),
        title='[bold underline]QuickStart_Rhy'
        + "\n",
        show_header=False,
        show_edge=False,
        box=SIMPLE,
    )

    for line in lines:
        tb.add_row('qs ' + line[0], lang_detector[line[0]] + lang_detector['tools_help'], line[1])
    qs_default_console.print(tb, justify="center")

def menu_table(group):
    from rich.table import Table, Column
    from rich.box import SIMPLE

    table = {
        'basic': basic_funcs,
        'system': system_funcs,
        'net': net_funcs,
        'api': api_funcs,
        'image': image_funcs,
    }[group]

    table.pop('self')
    tb = Table(
        *(
            [
                Column("1", style="bold magenta", justify="left"),
                Column("2", style="bold yellow", justify="right"),
            ]
        ),
        title=f'[bold underline]{group}'
        + "\n",
        show_header=False,
        show_edge=False,
        box=SIMPLE,
    )
    for key in table:
        if key in ['mktar', 'mkzip', 'mk7z']:
            tb.add_row(f"qs {key}", f"{lang_detector['compress'].format(key)}")
        elif key in ['unzip', 'untar', 'un7z', 'unrar']:
            tb.add_row(f"qs {key}", f"{lang_detector['decompress'].format(key)}")
        elif key in ['md5', 'sha1', 'sha256', 'sha512']:
            tb.add_row(f"qs {key}", f"{lang_detector['hashCal'].format(key)}")
        else:
            tb.add_row(f"qs {key}", f"{lang_detector['menu_' + key]}")
    qs_default_console.print(tb, justify="center")


def command_help(command):
    """
    """
    if val := cmd_table[command][command][1]:
        qs_default_console.print(f'[bold cyan][{lang_detector["usage"]}][/] qs {command} {val}')


basic_funcs = {
    "self": ".",
    "u": ["open_url", "<urls...>"],
    "a": ["open_app", "<app> [files...]"],
    "f": ["open_file", "<files...>"],
    "time": ["cur_time", ""],
    "cal": ["calculate", "<expression>"],
    "pcat": ["pcat", ""],
    "fcopy": ["fcopy", "<file>"],
    "tcopy": ["tcopy", "<text>"],
    "copy": ["copy", "<file>"],
    "play": ["play_music", "<audio>"],
    "lp": ["qs_print", "<file>"],
    "sas": ["sas", ""],
    "swap": ["swap", "<file1> <file2>"],
}

system_funcs = {
    "self": ".system",
    "top": ["top", ""],
    "go2git": ["go_github", ""],
    "mktar": ["mktar", "<files or dirs...>"],
    "untar": ["untar", "<tar file>"],
    "mkzip": ["mkzip", "<files or dirs...>"],
    "unzip": ["unzip", "<zip file>"],
    "unrar": ["unrar", "<rar file>"],
    "mk7z": ["mk7z", "<files or dirs...>"],
    "un7z": ["un7z", "<7z file>"],
    "md5": ["md5", "<file>"],
    "sha1": ["sha1", "<file>"],
    "sha256": ["sha256", "<file>"],
    "sha512": ["sha512", "<file>"],
    "diff": ["diff_dir", "<dir1> <dir2>"],
    "mount": ["mount_dmg", "<dmg file>"],
    "unmount": ["unmount_dmg", ""],
}

net_funcs = {
    "self": ".netTools",
    "http": ["http", "[<ip>:<port>] [-bind <url>]"],
    "dl": ["download", f"""[url (in clipboard)]
      [--video] | [-v]    :-> {lang_detector['using_youtube_dl']}
      [--proxy] | [-px]   :-> {lang_detector['using_proxy']}
      [--name <fileName>] :-> {lang_detector['set_filename']}
      [--referer] | [-e] <url> :-> {lang_detector['set_referer']}
"""],
    "wifi": ["wifi", ""],
    "upgrade": ["upgrade", ""],
    "netinfo": ["netinfo", "<ip | domain | url>"],
    "surl": ["scan_url", "<url>"],
}

api_funcs = {
    "self": ".apiTools",
    "trans": ["translate", "<text (or in clipboard)>"],
    "pinyin": ["pinyin", "<text (or in clipboard)>"],
    "rmbg": ["remove_bg", "<image file>"],
    "smms": ["smms", "<image or markdown file>"],
    "alioss": ["ali_oss", f"""\
          -up <file> [bucket] :-> {lang_detector['upload_to_bucket']}
          -dl <file> [bucket] :-> {lang_detector['download_from_bucket']}
          -rm <file> [bucket] :-> {lang_detector['remove_from_bucket']}
          -ls [bucket]        :-> {lang_detector['list_bucket']}"""],
    "qiniu": ["qiniu", f"""\
          -up <file> [bucket] :-> {lang_detector['upload_to_bucket']}
          -dl <file> [bucket] :-> {lang_detector['download_from_bucket']}
          -rm <file> [bucket] :-> {lang_detector['remove_from_bucket']}
          -ls [bucket]        :-> {lang_detector['list_bucket']}"""],
    "txcos": ["txcos", f"""\
          -up <file> [bucket] :-> {lang_detector['upload_to_bucket']}
          -dl <file> [bucket] :-> {lang_detector['download_from_bucket']}
          -rm <file> [bucket] :-> {lang_detector['remove_from_bucket']}
          -ls [bucket]        :-> {lang_detector['list_bucket']}"""],
    "LG": ["largeImage", "<image file>"],
    "weather": ["weather", "[city]"],
    "nlp": ["AipNLP", "<text (or in clipboard)>"],
    "bcv": ["bili_cover", "<video id or url>"],
    "gbc": ["gbc", "<garbage name>"],
    "svi": ["short_video_info", "<url>"],
    "svd": ["short_video_dl", "<url>"],
    "acg": ["acg", "[--save]"],
    "bing": ["bingImg", "[--save]"],
    "phi": ["preview_html_images", "<url> [--save]"],
    "kd": ["kdCheck", "<courier id>"],
    "loli": ["loli", "[--save] [-p]"],
    "setu": ["setu", "[--save] [-p]"],
    "exc": ["exchange", "<num> <from> | eg. \"qs exc 100 USD\""],
    "zhihu": ["zhihuDaily", ""],
    "wallhaven": ["wallhaven", "[--save] [-one] [--url <url>]"],
    "lmgtfy": ["lmgtfy", "<keywords>"],
    "d60": ["daily60s", "[--save]"],
    "m2t": ["m2t", "<magnet url>"],
    "d2m": ["d2m", "<keywords>"],
    "doutu": ["doutu", "<keywords>"],
    "joke": ["joke", ""],
    "gpt": ["gpt", "[--translate]"],
    "pushdeer": ["pushdeer", "[text]"],
}

image_funcs = {
    "self": ".imageDeal",
    "stbg": ["set_img_background", "<image> <to color> \[from color]"],
    "icat": ["icat", "<image file or url>"],
    "v2gif": ["v2gif", "<video file> [size] [fps]"],
    "rmaudio": ["remove_audio", "<video file>"],
    "v2mp4": ["v2mp4", "<video file>"],
    "v2mp3": ["v2mp3", "<video file>"],
    "i2png": ["i2png", "<image file>"],
    "i2jpg": ["i2jpg", "<image file>"],
    "i2pdf": ["i2pdf", "<image file>"],
    "fmti": ["fmt_img_color", "<image file> <to color> [exclude colors...]"],
    "vsta": ["vsta", "<video file>"],
}


cmd_table = {
    j: i
    for i in [basic_funcs, api_funcs, net_funcs, image_funcs, system_funcs]
    for j in i
    if j != "self"
}
