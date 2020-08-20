# coding=utf-8
import os
import sys
import json


name = 'QuickStart_Rhy'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) '
                  'Version/11.0.2 Safari/604.4.7'}
system = sys.platform
if system.startswith('win'):
    dir_char = '\\'
else:
    dir_char = '/'

user_root = os.path.expanduser('~') + dir_char
if os.path.exists(user_root + '.qsrc'):
    with open(user_root + '.qsrc', 'r', encoding='utf8') as f:
        qs_config = json.loads(f.read(), encoding='utf8')
else:
    with open(user_root + '.qsrc', 'w') as f:
        f.write("""{
  "basic_settings": {
    "default_language": "zh",
    "default_translate_engine": {
      "index": 0,
      "support": ["default", "TencentCloud"]
    },
    "default_proxy": "user:password@ip:port or ip:port"
  },
  "API_settings": {
    "rmbg": "GET: https://www.remove.bg",
    "smms": "GET: https://sm.ms",
    "darksky": "GET: https://darksky.net/",
    "aliyun_oss_acid": "GET: https://www.aliyun.com/product/oss",
    "aliyun_oss_ackey": "GET: https://www.aliyun.com/product/oss",
    "aliyun_oss_bucket_url": "GET: https://www.aliyun.com/product/oss",
    "aliyun_oss_df_bucket": "GET: https://www.aliyun.com/product/oss",
    "txyun_scid": "GET: https://console.cloud.tencent.com/",
    "txyun_sckey": "GET: https://console.cloud.tencent.com/",
    "txyun_cos_df_bucket": "GET: https://console.cloud.tencent.com/",
    "txyun_df_region": "GET: ap-[location]",
    "qiniu_ac_key": "GET: http://qiniu.com/",
    "qiniu_sc_key": "GET: http://qiniu.com/",
    "qiniu_bk_name": "GET: [Qiniu Bucket Name]",
    "gitee": "GET: http://gitee.com/",
    "ipinfo": "GET: https://ipinfo.io/",
    "AipImageAPP_ID": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipImageAPP_KEY": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipImageSECRET_KEY": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipNlpAPP_ID" : "GET: https://cloud.baidu.com/product/nlp_apply",
    "AipNlpAPP_KEY": "GET: https://cloud.baidu.com/product/nlp_apply",
    "AipNlpSECRET_KEY": "GET: https://cloud.baidu.com/product/nlp_apply",
    "seafile_communicate_path": "GET: /Path/to/file",
    "alapi_token": "GET: https://user.alapi.cn/"
  }
}
""")
    qs_config = {}
    exit("You need set qs configure at: ~/.qsrc when you first run!")
user_lang = qs_config['basic_settings']['default_language']
trans_engine = qs_config['basic_settings']['default_translate_engine']['support']
trans_engine = trans_engine[qs_config['basic_settings']['default_translate_engine']['index']]


def deal_ctrl_c(signum, frame):
    """
    默认的处理ctrl c的函数

    default function to deal [CTRL C]

    :param signum: signum
    :param frame: frame
    :return: None
    """
    if signum or frame or True:
        exit(0)


def remove(path):
    """
    删除文件或文件夹

    delete file or folder.

    :param path: 路径
    :return: None
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        else:
            os.remove(path)


def cur_time():
    """
    获取当前时间

    get time of now

    :return: None
    """
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
    """
    打开命令行参数中的链接

    open urls in argv

    :return: None
    """
    import webbrowser as wb
    from QuickStart_Rhy.NetTools import formatUrl
    if sys.argv[2:]:
        for url in sys.argv[2:]:
            url = formatUrl(url)
            wb.open_new_tab(url)
    else:
        import pyperclip
        try:
            url = pyperclip.paste()
        except :
            url = input('Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: '
                        if user_lang != 'zh' else '抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:')
        wb.open_new_tab(formatUrl(url))


def open_app():
    """
    Mac OS下的open（不支持其他平台）

    open app (only support Mac OS)

    :return: None
    """
    if system == 'darwin':
        os.system('open -a ' + ' '.join(sys.argv[2:]))
    else:
        print('"-a" is only support Mac OS X')


def open_file(argv=None):
    """
    使用合适应用打开文件

    Open file with appropriate application

    :return: None
    """
    import webbrowser as wb

    if not argv:
        argv = sys.argv[2:]
    if system == 'darwin':
        os.system('open "' + '" "'.join(argv) + '"')
    else:
        for file in argv:
            if os.path.exists(file):
                path = os.path.abspath(file)
                wb.open('file://%s' % path)


def init():
    import webbrowser as wb
    wb.open('http://login.cup.edu.cn')


def calculate():
    """
    执行算数表达式

    Execute the arithmetic expression.

    :return: None
    """
    try:
        exp = ' '.join(sys.argv[2:])
        print('%s = %s' % (exp, eval(exp)))
    except Exception as e:
        exit('[ERROR] %s' % repr(e))
