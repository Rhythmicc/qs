# coding=utf-8
import sys
from QuickStart_Rhy import user_lang


def remove_bg():
    """
    删除图片背景

    Delete image background
    """
    try:
        path = sys.argv[2]
    except IndexError:
        exit('Usage: qs -rmbg picture')
    else:
        if path == '-help':
            print('Usage: qs -rmbg picture')
            return
        from QuickStart_Rhy.API.SimpleAPI import rmbg
        rmbg(path)


def smms():
    """
    上传图片或Markdown中图片到smms

    Upload images or Markdown images to SMMS
    """
    try:
        path = sys.argv[2]
    except IndexError:
        exit('Usage: qs -smms [picture | *.md]')
    else:
        if path == '-help':
            print('Usage: qs -smms [picture | *.md]')
            return
        from QuickStart_Rhy.API.SimpleAPI import smms
        smms(path)


def up_img():
    """
    上传图片或Markdown中图片到多平台（不保证数据安全）

    Upload images or Markdown images to multiple platforms (data security is not guaranteed)
    """
    try:
        path = sys.argv[2]
    except IndexError:
        exit('Usage: qs -upload_image [picture]')
    else:
        from QuickStart_Rhy.API.alapi import upload_image
        import random
        spt_type = {'Ali': '阿里云', 'Sogou': '搜狗', 'Vimcn': 'Vim-cn.com', 'Niupic': '牛图', 'Juejin': '掘进',
                    'UploadLiu': 'upload.ouliu.net', 'Catbox': 'catbox', 'NetEasy': '网易', 'Prnt': 'Prnt',
                    'Qihoo': '360奇虎', 'Souhu': '搜狐', 'Toutiao': '头条', 'Xiaomi': '小米', 'ImgTg': 'imt.tg'}
        spt_type_keys = list(spt_type.keys())
        if path == '-help':
            print('Usage: qs -upload_image <picture | *.md> [platform]\n\nSupport ([platform]: description):')
            print(''.join(['%-10s: %s%s' % (spt_type_keys[i], spt_type[spt_type_keys[i]], '\t' if (i + 1) % 3 else '\n')
                           for i in range(len(spt_type_keys))]))
            print('\n[NOTE] If you do not set platform, qs will randomly choose one.')
            return
        type_map = {}
        for i in spt_type:
            type_map[i.lower()] = i
        argv_len_3 = len(sys.argv) > 3
        if argv_len_3:
            sys.argv[3] = sys.argv[3].lower()
        upload_image(path, type_map[sys.argv[3]]) if argv_len_3 and sys.argv[3] in type_map else (
            upload_image(path, random.choice(spt_type_keys)),
            print('No such platform: %s' % sys.argv[3]) if argv_len_3 else 1
        )


def ali_oss():
    """
    阿里云对象存储

    Ali Cloud object storage
    """
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
        from QuickStart_Rhy.API.AliCloud import AliyunOSS
        ali_api = AliyunOSS()
        func_table = ali_api.get_func_table()
        if not file:
            func_table[op](bucket)
        else:
            func_table[op](file, bucket)


def qiniu():
    """
    七牛云对象存储

    Qiniu cloud object storage
    """
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
        from QuickStart_Rhy.API.QiniuOSS import QiniuOSS
        qiniu_api = QiniuOSS()
        func_table = qiniu_api.get_func_table()
        if not file:
            func_table[op](bucket)
        else:
            func_table[op](file, bucket)


def txcos():
    """
    腾讯云对象存储

    Tencent Cloud object storage
    """
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
        from QuickStart_Rhy.API.TencentCloud import TxCOS
        tx_api = TxCOS()
        func_table = tx_api.get_func_table()
        if not file:
            func_table[op](bucket)
        else:
            func_table[op](file, bucket)


def translate():
    """
    qs默认的翻译引擎

    Qs default Translation engine
    """
    global Translate, translate
    from QuickStart_Rhy import trans_engine
    import pyperclip
    if trans_engine != 'default':
        from QuickStart_Rhy.API.TencentCloud import Translate
    else:
        from QuickStart_Rhy.API.alapi import translate

    content = ' '.join(sys.argv[2:])
    if not content:
        try:
            content = pyperclip.paste()
        except:
            content = input('Sorry, but your system is not supported by `pyperclip`\nSo you need input content '
                            'manually: '
                            if user_lang != 'zh' else '抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:')
    if content:
        if trans_engine == 'TencentCloud':
            ret = Translate().translate(content.replace('\n', ' '))
        else:
            ret = translate(content.replace('\n', ' '))
        print(ret if ret else 'Translate Failed!')
    else:
        print("No content in your clipboard or command parameters!")


def weather():
    """查天气 | Check weather"""
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
    tls = [ThreadFunctionWrapper(get_data, 'https://wttr.in/' + (loc if loc else '?lang={}'.format(user_lang))),
           ThreadFunctionWrapper(get_data, 'https://v2.wttr.in/' + loc)]
    for i in tls:
        i.start()
    for i in tls:
        i.join()
    simple = tls[0].get_res()
    table = tls[1].get_res()
    if simple:
        if not loc:
            if user_lang == 'zh':
                from QuickStart_Rhy.API.alapi import translate
                trans_loaction = translate(simple[0].split('：')[-1])
                print('地区：' + trans_loaction if trans_loaction else simple[0].split('：')[-1])
            else:
                print('Location' + simple[0][simple[0].index(':'):])
        simple = simple[2:7]
        print('\n'.join(simple))
    else:
        print('Error: Get data failed.' if user_lang != 'zh' else '错误: 获取数据失败')
    if table:
        print(table[3][:-1])
        bottom_line = 7
        try:
            while '╂' not in table[bottom_line]:
                bottom_line += 1
        except IndexError:
            exit('Get Weather Data failed!' if user_lang != 'zh' else '获取天气数据失败')
        for i in table[7:bottom_line + 2]:
            print(i[:-1])
        print('└────────────────────────────────────────────────────────────────────────')
        print('\n'.join(table[-3 if not loc else -4:]))
    else:
        print('Error: Get data failed.' if user_lang != 'zh' else '错误: 获取数据失败')


def ipinfo(ip: str = None):
    """
    通过ipinfo查ip（定位不准）

    Check IP via IPInfo (incorrect location)
    """
    from QuickStart_Rhy.API.IpInfo import get_ip_info
    return get_ip_info(ip)


def largeImage():
    """
    百度图片效果增强

    Baidu picture effect enhancement
    """
    try:
        path = sys.argv[2]
    except IndexError:
        exit('Usage qs -LG img')
    else:
        from QuickStart_Rhy.API.BaiduCloud import ImageDeal
        aip_cli = ImageDeal()
        aip_cli.largeImage(path)


def AipNLP():
    """百度NLP | Baidu NLP"""
    from QuickStart_Rhy.API.BaiduCloud import AipNLP
    import pyperclip
    ct = sys.argv[2:]
    if not ct:
        try:
            ct = [pyperclip.paste()]
        except :
            ct = [input('Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: '
                        if user_lang != 'zh' else '抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:')]
    NLP = AipNLP()
    for _id, line in enumerate(ct):
        ct[_id] = NLP.get_res(line)
        if _id == 9:
            print('...')
        elif _id < 9:
            print(ct[_id])
    try:
        pyperclip.copy('\n'.join(ct))
    except:
        pass


def Seafile_Communicate():
    """Seafile做共享粘贴板"""
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
    """Pasteme信息传递"""
    from QuickStart_Rhy.API.SimpleAPI import pasteme
    try:
        method = sys.argv[2]
        key = sys.argv[3]
        password = sys.argv[4] if len(sys.argv) > 4 else ''
        pasteme(key, password, method)
    except IndexError:
        print("Usage:\n  1. qs -pasteme get key [password]\n  2. qs -pasteme post lang [password]")
        exit(0)


def bili_cover():
    """下载Bilibili视频、直播的封面图片（视频链接、视频号均可识别）"""
    from QuickStart_Rhy.API.alapi import bili_cover as bc
    import pyperclip

    try:
        url = sys.argv[2]
    except IndexError:
        try:
            url = pyperclip.paste()
        except :
            print('Sorry, but your system may not be suppported by `pyperclip`')
            return
    if not url:
        exit('Usage: qs -bcv <url/video code>')
    bc(url)


def gbc():
    """查询中国垃圾分类（且仅支持中文查询）"""
    from QuickStart_Rhy.API.alapi import garbage_classification
    try:
        print(garbage_classification(sys.argv[2:]))
    except :
        exit('Usage: qs -gbc <garbage...>')
