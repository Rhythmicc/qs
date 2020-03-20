import sys


def remove_bg():
    try:
        path = sys.argv[2]
    except IndexError:
        exit('Usage: %s -rmbg picture' % sys.argv[0])
    else:
        from QuickStart_Rhy.API.simple_api import rmbg
        rmbg(path)


def ImgBed():
    try:
        path = sys.argv[2]
    except IndexError:
        exit('Usage: %s -smms [picture]' % sys.argv[0])
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
        print('qs -ali_nas:\n'
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


def translate():
    import pyperclip
    from QuickStart_Rhy.API.Dict import Dict

    content = ' '.join(sys.argv[2:])
    if not content:
        content = pyperclip.paste()
    if content:
        content.replace('\n', ' ')
        translator = Dict()
        ret = translator.dictionary(content)
        print(ret['trans_result']['data'][0]['dst'])
    else:
        print("No content in your clipboard or command parameters!")


def weather():
    import threading
    from QuickStart_Rhy.basic import headers, dir_char
    import requests

    class pull_data(threading.Thread):
        def __init__(self, url):
            threading.Thread.__init__(self)
            self.url = url
            self.ret = []

        def run(self):
            try:
                ct = requests.get(self.url, headers)
            except:
                return
            ct.encoding = 'utf-8'
            ct = ct.text.split('\n')
            if dir_char == '/':
                self.ret = ct.copy()
            else:
                import re
                for line in range(len(ct)):
                    ct[line] = re.sub('\x1b.*?m', '', ct[line])
                self.ret = ct.copy()

        def get_ret(self):
            return self.ret

    try:
        loc = sys.argv[2]
    except IndexError:
        loc = ''
    tls = [pull_data('https://wttr.in/' + (loc if loc else '?lang=zh')), pull_data('https://v2.wttr.in/' + loc)]
    for i in tls:
        i.start()
        i.join()
    simple = tls[0].get_ret()
    table = tls[1].get_ret()
    if simple:
        if not loc:
            from QuickStart_Rhy.API.Dict import Dict
            translator = Dict()
            try:
                print('地区：' + translator.dictionary(simple[0].split('：')[-1])['trans_result']['data'][0]['dst'])
            except:
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
