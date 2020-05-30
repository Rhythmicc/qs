import colorama
from colorama import Fore, Style
colorama.init()


def color_rep(ss):
    ss = ss.strip('\n').split('\n')
    for i, line in enumerate(ss):
        if ':->' in line:
            line = line.split(':->')
            line = Fore.LIGHTMAGENTA_EX + line[0] + Style.RESET_ALL + ':->' + Fore.YELLOW + line[1] + Style.RESET_ALL
        if '|' in line:
            line = line.split('|')
            line = line[0] + Style.RESET_ALL + '|' + Fore.GREEN + line[1] + Style.RESET_ALL
        ss[i] = line
    return '\n'.join(ss)


def base_menu():
    print(color_rep("""Basic Tools help:
    qs -u  <url>              :-> open url using default browser
    qs -a  <app> [file..]     :-> open app or open file by app(for Mac OS X)
    qs -f  <file...>          :-> open file by default app
    qs -cal exp               :-> calculate exp
    qs -time                  :-> view current time"""))


def system_menu():
    print(color_rep("""System Tools help:
    qs -top                   :-> cpu and memory monitor
    qs -mktar <path...>       :-> create gzipped archive for path
    qs -untar <path>          :-> extract path.tar.*
    qs -mkzip <path...>       :-> make a zip for path
    qs -unzip <path>          :-> unzip path.zip"""))


def net_menu():
    print(color_rep("""Net Tools help:
    qs -http [ip] [-bind url] :-> start a multithread ftp server
    qs -dl [urls]             :-> download file from url(in clipboard)
    qs -upload                :-> upload your pypi library
    qs -upgrade               :-> update qs"""))


def api_menu():
    print(color_rep("""API Tools help:
    qs -trans [content]       :-> translate the content(in clipboard)
    qs -rmbg <picture>        :-> remove image background
    qs -smms <picture/*.md>   :-> upload img to smms or all in .md
    qs -alioss -help          :-> get aliyun oss api help menu
    qs -txcos -help           :-> get tencent cos api help menu
    qs -qiniu -help           :-> get qiniu oss api help menu
    qs -weather [address]     :-> check weather (of address)
    qs -LG <image>            :-> make image larger(with AI)
    qs -nlp [words]           :-> Text(or in clipboard) error correction
    qs -sea [method] [msg]    :-> Get Or Post msg by Seafile.
    qs -pasteme [method] [*]  :-> get with key, [password] or post clipboard content"""))


def image_menu():
    print(color_rep("""Image Tools help:
    qs -stbg pic to [from]    :-> color replace for picture
    qs -v2gif path [sz] [fps] :-> generate gif from video
    qs -v2mp4 <video>         :-> format video to mp4
    qs -rmaudio <video>       :-> remove audio in video (return mp4 only)"""))


menu_table = {
    '-basic': base_menu,
    '-system': system_menu,
    '-net': net_menu,
    '-api': api_menu,
    '-image': image_menu
}


basic_funcs = {
    'self': 'basic',
    '-u': 'u',
    '-a': 'open_app',
    '-f': 'open_file',
    '-i': 'init',
    '-time': 'cur_time',
    '-cal': 'calculate'
}

system_funcs = {
    'self': 'system',
    '-top': 'top',
    '-mktar': 'mktar',
    '-untar': 'untar',
    '-mkzip': 'mkzip',
    '-unzip': 'unzip',
}

net_funcs = {
    'self': 'nettools',
    '-http': 'http',
    '-dl': 'download',
    '-upgrade': 'upgrade',
    '-upload': 'upload_pypi'
}

api_funcs = {
    'self': 'api',
    '-trans': 'translate',
    '-rmbg': 'remove_bg',
    '-smms': 'ImgBed',
    '-alioss': 'ali_oss',
    '-qiniu': 'qiniu',
    '-txcos': 'txcos',
    '-LG': 'largeImage',
    '-weather': 'weather',
    '-nlp': 'AipNLP',
    '-sea': 'Seafile_Communicate',
    '-pasteme': 'Pasteme'
}

image_funcs = {
    'self': 'imagedeal',
    '-stbg': 'set_img_background',
    '-v2gif': 'v2gif',
    '-rmaudio': 'rmaudio',
    '-v2mp4': 'v2mp4'
}
