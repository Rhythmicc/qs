import sys


def remove_bg():
    try:
        path = sys.argv[2]
    except IndexError:
        exit('Usage: qs -rmbg picture')
    else:
        from QuickStart_Rhy.API.simple_api import rmbg
        rmbg(path)


def ImgBed():
    try:
        path = sys.argv[2]
    except IndexError:
        exit('Usage: qs -smms [picture]')
    else:
        from QuickStart_Rhy.API.simple_api import smms
        smms(path)


def ali_oss():
    try:
        op = sys.argv[2]
        if op not in ['-dl', '-up', '-ls', '-rm']:
            raise IndexError
        file = sys.argv[3] if op != '-ls' else None
        try:
            bucket = sys.argv[4] if op != '-ls' else sys.argv[3]
        except IndexError:
            bucket = None
    except IndexError:
        print('qs -alioss:\n'
              '\t-up <file> [bucket]: upload file to bucket\n'
              '\t-dl <file> [bucket]: download file from bucket\n'
              '\t-rm <file> [bucket]: remove file in bucket\n'
              '\t-ls [bucket]       : get file info of bucket')
        exit(0)
    else:
        from QuickStart_Rhy.API.Aliyun_oss import Aliyun_oss_api
        ali_api = Aliyun_oss_api()
        func_table = ali_api.get_func_table()
        if not file:
            func_table[op](bucket)
        else:
            func_table[op](file, bucket)


def qiniu():
    try:
        op = sys.argv[2]
        if op not in ['-up', '-rm', '-cp', '-ls', '-dl']:
            raise IndexError
        file = sys.argv[3] if op != '-ls' else None
        try:
            bucket = sys.argv[4] if op != '-ls' else sys.argv[3]
        except IndexError:
            bucket = None
    except IndexError:
        print('qs -qiniu:\n'
              '\t-up <file> [bucket]: upload file to bucket\n'
              '\t-rm <file> [bucket]: remove file in bucket\n'
              '\t-cp <url > [bucket]: copy file from url\n'
              '\t-dl <file> [bucket]: download file from bucket\n'
              '\t-ls [bucket]       : get file info of bucket')
        exit(0)
    else:
        from QuickStart_Rhy.API.Qiniu_oss import Qiniu_oss_api
        qiniu_api = Qiniu_oss_api()
        func_table = qiniu_api.get_func_table()
        if not file:
            func_table[op](bucket)
        else:
            func_table[op](file, bucket)


def txcos():
    try:
        op = sys.argv[2]
        if op not in ['-dl', '-up', '-ls', '-rm']:
            raise IndexError
        file = sys.argv[3] if op != '-ls' else None
        try:
            bucket = sys.argv[4] if op != '-ls' else sys.argv[3]
        except IndexError:
            bucket = None
    except IndexError:
        print('qs -txcos:\n'
              '\t-up <file> [bucket]: upload file to bucket\n'
              '\t-dl <file> [bucket]: download file from bucket\n'
              '\t-rm <file> [bucket]: remove file in bucket\n'
              '\t-ls [bucket]       : get file info of bucket')
        exit(0)
    else:
        from QuickStart_Rhy.API.txcos import txcos
        tx_api = txcos()
        func_table = tx_api.get_func_table()
        if not file:
            func_table[op](bucket)
        else:
            func_table[op](file, bucket)


def translate():
    import pyperclip
    from QuickStart_Rhy.API.TencentTranslate import Translate

    content = ' '.join(sys.argv[2:])
    if not content:
        content = pyperclip.paste()
    if content:
        content.replace('\n', ' ')
        translator = Translate()
        ret = translator.translate(content)
        print(ret if ret else 'Translate Failed!')
    else:
        print("No content in your clipboard or command parameters!")


def weather():
    from QuickStart_Rhy import headers, dir_char
    from QuickStart_Rhy.ThreadTools import ThreadFunctionWrapper
    import requests

    def get_data(url):
        try:
            ct = requests.get(url, headers)
        except:
            return
        ct.encoding = 'utf-8'
        ct = ct.text.split('\n')
        if dir_char == '/':
            res = ct.copy()
        else:
            import re
            for line in range(len(ct)):
                ct[line] = re.sub('\x1b.*?m', '', ct[line])
            res = ct.copy()
        return res

    try:
        loc = sys.argv[2]
    except IndexError:
        loc = ''
    tls = [ThreadFunctionWrapper(get_data, 'https://wttr.in/' + (loc if loc else '?lang=zh')),
           ThreadFunctionWrapper(get_data, 'https://v2.wttr.in/' + loc)]
    for i in tls:
        i.start()
    for i in tls:
        i.join()
    simple = tls[0].get_res()
    table = tls[1].get_res()
    if simple:
        if not loc:
            from QuickStart_Rhy.API import pre_check
            if pre_check("txyun_scid", False) and pre_check("txyun_sckey", False):
                from QuickStart_Rhy.API.TencentTranslate import Translate
                translator = Translate()
                trans_loaction = translator.translate(simple[0].split('：')[-1])
                print('地区：' + trans_loaction if trans_loaction else simple[0].split('：')[-1])
            else:
                print('地区：' + simple[0].split('：')[-1])
        simple = simple[2:7]
        print('\n'.join(simple))
    else:
        print('Error: Get data failed.')
    if table:
        print(table[3][:-1])
        bottom_line = 7
        try:
            while '╂' not in table[bottom_line]:
                bottom_line += 1
        except IndexError:
            exit('Get Weather Data failed!')
        for i in table[7:bottom_line + 2]:
            print(i[:-1])
        print('└────────────────────────────────────────────────────────────────────────')
        print('\n'.join(table[-3 if not loc else -4:]))
    else:
        print('Error: Get detail failed.')


def ipinfo(ip: str = None):
    from QuickStart_Rhy.API.IPinfo import get_ip_info
    return get_ip_info(ip)


def largeImage():
    try:
        path = sys.argv[2]
    except IndexError:
        exit('Usage qs -LG img')
    else:
        from QuickStart_Rhy.API import AipImage
        aip_cli = AipImage.ImageDeal()
        aip_cli.largeImage(path)


def AipNLP():
    from QuickStart_Rhy.API.AipNLP import AipNLP
    import pyperclip
    ct = sys.argv[2:]
    if not ct:
        ct = [pyperclip.paste()]
    NLP = AipNLP()
    for id, line in enumerate(ct):
        ct[id] = NLP.get_res(line)
        if id == 9:
            print('...')
        elif id < 9:
            print(ct[id])
    pyperclip.copy('\n'.join(ct))


def Seafile_Communicate():
    from QuickStart_Rhy.API.Seafile import Seafile
    try:
        method = sys.argv[2]
        if method == 'get':
            Seafile().get_msg()
        elif method == 'post':
            msg = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else None
            Seafile().post_msg(msg) if msg else Seafile().post_msg()
    except IndexError:
        print("Usage:\n  1. qs -sea get\n  2. qs -sea post [msg]")
        exit(0)


def Pasteme():
    from QuickStart_Rhy.API.simple_api import pasteme
    try:
        method = sys.argv[2]
        key = sys.argv[3]
        password = sys.argv[4] if len(sys.argv) > 4 else ''
        pasteme(key, password, method)
    except IndexError:
        print("Usage:\n  1. qs -pasteme get key [password]\n  2. qs -pasteme post lang [password]")
        exit(0)
