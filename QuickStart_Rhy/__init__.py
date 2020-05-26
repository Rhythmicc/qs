import os
import sys


name = 'QuickStart_Rhy'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) '
                  'Version/11.0.2 Safari/604.4.7'}
system = sys.platform
if system.startswith('win'):
    dir_char = '\\'
else:
    dir_char = '/'


def deal_ctrl_c(signum, frame):
    if signum or frame or True:
        exit(0)


def remove(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        else:
            os.remove(path)


def cur_time():
    week = {
        'Monday': '周一',
        'Tuesday': '周二',
        'Wednesday': '周三',
        'Thursday': '周四',
        'Friday': '`周五',
        'Saturday': '周六',
        'Sunday': '周日'
    }
    import time
    tm = time.strftime('%Y年%m月%d日 %A %H:%M:%S', time.localtime(time.time())).split()
    tm[1] = week[tm[1]]
    print(' '.join(tm))


def u():
    import webbrowser as wb
    from QuickStart_Rhy.NetTools import formatUrl
    if sys.argv[2:]:
        for url in sys.argv[2:]:
            url = formatUrl(url)
            wb.open_new_tab(url)
    else:
        import pyperclip
        url = pyperclip.paste()
        wb.open_new_tab(formatUrl(url))


def open_app():
    if system == 'darwin':
        os.system('open -a ' + ' '.join(sys.argv[2:]))
    else:
        print('"-a" is only support Mac OS X')


def open_file():
    import webbrowser as wb
    if system == 'darwin':
        os.system('open "' + '" "'.join(sys.argv[2:]) + '"')
    else:
        for file in sys.argv[2:]:
            if os.path.exists(file):
                path = os.path.abspath(file)
                wb.open('file://%s' % path)


def init():
    import webbrowser as wb
    wb.open('http://login.cup.edu.cn')


def calculate():
    try:
        exp = ' '.join(sys.argv[2:])
        print('%s = %s' % (exp, eval(exp)))
    except Exception as e:
        exit('[ERROR] %s' % repr(e))
