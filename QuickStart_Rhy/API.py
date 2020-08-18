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
        exit('%s: qs -rmbg <%s>' % (('Usage', 'picture') if user_lang != 'zh' else ('用法', '图像')))
    else:
        if path == '-help':
            print('%s: qs -rmbg <%s>' % (('Usage', 'picture') if user_lang != 'zh' else ('用法', '图像')))
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
        exit('%s: qs -smms <%s>' % (('Usage', 'picture | *.md') if user_lang != 'zh' else ('用法', '图像 | *.md')))
    else:
        if path == '-help':
            print('%s: qs -smms <%s>' % (('Usage', 'picture | *.md') if user_lang != 'zh' else ('用法', '图像 | *.md')))
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
        exit('%s: qs -upimg <%s>' % (('Usage', 'picture | *.md') if user_lang != 'zh' else ('用法', '图像 | *.md')))
    else:
        from QuickStart_Rhy.API.alapi import upload_image
        import random
        spt_type = {'ali': '阿里云', 'sogou': '搜狗', 'alapi': 'Alapi',
                    'qihoo': '360奇虎', 'toutiao': '头条', 'xiaomi': '小米', 'imgTg': 'imt.tg'}
        spt_type_keys = list(spt_type.keys())
        if path == '-help' or path == '-h':
            print('Usage: qs -upimg <picture | *.md> [platform]\n\nSupport ([platform]: description):'
                  if user_lang != 'zh' else
                  '用法: qs -upimg <图像 | *.md> [平台]\n\n支持 ([可选平台]: 描述):')
            print(''.join(['%14s' % '%s: %s%s' % (
                spt_type_keys[i], spt_type[spt_type_keys[i]], '\t' if (i + 1) % 3 else '\n'
            ) for i in range(len(spt_type_keys))]))
            print('\n[NOTE] If you do not set platform, qs will randomly choose one.' if user_lang != 'zh' else
                  '\n[提示] 如果你没有设置平台，qs将随机抽取一个可用平台')
            return
        type_map = {}
        for i in spt_type:
            type_map[i.lower()] = i
        argv_len_3 = len(sys.argv) > 3
        if argv_len_3:
            sys.argv[3] = sys.argv[3].lower()
        upload_image(path, type_map[sys.argv[3]]) if argv_len_3 and sys.argv[3] in type_map else (
            upload_image(path, random.choice(spt_type_keys)),
            print(('No such platform: %s' if user_lang != 'zh' else '没有这个平台: %s') % sys.argv[3]) if argv_len_3 else 1
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
              '    -up <file> [bucket]: upload file to bucket\n'
              '    -dl <file> [bucket]: download file from bucket\n'
              '    -rm <file> [bucket]: remove file in bucket\n'
              '    -ls [bucket]       : get file info of bucket') \
            if user_lang != 'zh' else \
            print('qs -alioss:\n'
                  '    -up <文件> [桶]: 上传文件至桶\n'
                  '    -dl <文件> [桶]: 从桶下载文件\n'
                  '    -rm <文件> [桶]: 从桶删除文件\n'
                  '    -ls [桶]       : 获取桶文件信息')
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
              '    -up <file> [bucket]: upload file to bucket\n'
              '    -dl <file> [bucket]: download file from bucket\n'
              '    -cp <url > [bucket]: copy file from url\n'
              '    -rm <file> [bucket]: remove file in bucket\n'
              '    -ls [bucket]       : get file info of bucket') \
            if user_lang != 'zh' else \
            print('qs -qiniu:\n'
                  '    -up <文件> [桶]: 上传文件至桶\n'
                  '    -dl <文件> [桶]: 从桶下载文件\n'
                  '    -cp <链接> [桶]: 从链接下载文件到桶\n'
                  '    -rm <文件> [桶]: 从桶删除文件\n'
                  '    -ls [桶]       : 获取桶文件信息')
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
              '    -up <file> [bucket]: upload file to bucket\n'
              '    -dl <file> [bucket]: download file from bucket\n'
              '    -rm <file> [bucket]: remove file in bucket\n'
              '    -ls [bucket]       : get file info of bucket') \
            if user_lang != 'zh' else \
            print('qs -txcos:\n'
                  '    -up <文件> [桶]: 上传文件至桶\n'
                  '    -dl <文件> [桶]: 从桶下载文件\n'
                  '    -rm <文件> [桶]: 从桶删除文件\n'
                  '    -ls [桶]       : 获取桶文件信息')
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
        print("No content in your clipboard or command parameters!"
              if user_lang != 'zh' else
              '剪贴板或命令参数没有内容!')


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
        exit('%s: qs -LG img' % 'Usage' if user_lang != 'zh' else '用法')
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
        except:
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
        print("Usage:\n  1. qs -sea get\n  2. qs -sea post [msg]"
              if user_lang != 'zh' else
              '用法:\n  1. qs -sea get\n  2. qs -sea post [消息]')
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
        print("Usage:\n  1. qs -pasteme get  key [password]\n  2. qs -pasteme post lang [password]"
              if user_lang != 'zh' else
              "用法:\n  1. qs -pasteme get  键值 [密码]\n  2. qs -pasteme post 语言 [密码]")
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
        except:
            print('Sorry, but your system may not be suppported by `pyperclip`'
                  if user_lang != 'zh' else
                  '抱歉，但是“pyperclip”不支持你的系统')
            return
    if not url:
        exit('Usage: qs -bcv <url/video code>'
             if user_lang != 'zh' else
             '用法: qs -bcv <链接/视频码>')
    bc(url)


def gbc():
    """查询中国垃圾分类（且仅支持中文查询）"""
    from QuickStart_Rhy.API.alapi import garbage_classification
    try:
        print(garbage_classification(sys.argv[2:]))
    except:
        exit('Usage: qs -gbc <garbage...>'
             if user_lang != 'zh' else
             '用法: qs -gbc <垃圾...>')


def short_video_info(son_call=False):
    """
    获取短视频信息 | Get short video information

    :return:
    """
    from QuickStart_Rhy.API.alapi import short_video_info
    from QuickStart_Rhy.NetTools import get_fileinfo, size_format
    import pyperclip
    try:
        url = sys.argv[2]
    except IndexError:
        try:
            url = pyperclip.paste()
        except:
            print('Sorry, but your system may not be suppported by `pyperclip`'
                  if user_lang != 'zh' else
                  '抱歉，但是“pyperclip”不支持你的系统')
            return
    if not url:
        exit('Usage: qs -svi <url/video code>' if not son_call else 'Usage: qs -svd <url/video code>')
    output_prefix = {
        'title': 'Title ' if user_lang != 'zh' else '标题',
        'video': 'Video ' if user_lang != 'zh' else '视频',
        'cover': 'Cover ' if user_lang != 'zh' else '封面',
        'source': 'Source' if user_lang != 'zh' else '来源'
    }
    status, res = short_video_info(url.strip('/'))
    if not status:
        print(res)
        print(res['title'] + ':' + res['source'])
        return status
    print('[{}] {}'.format(output_prefix['title'], res['title']))
    sz = int(get_fileinfo(res['video_url'])[-1].headers['Content-Length']) if not son_call else -1
    print('[{}] {}\n{}'.format(output_prefix['video'], size_format(sz, True) if sz > 0 else '--', res['video_url']))
    sz = int(get_fileinfo(res['cover_url'])[-1].headers['Content-Length'])
    print('\n[{}] {}\n{}'.format(output_prefix['cover'], size_format(sz, True), res['cover_url']))
    if 'source' in res:
        print('\n[{}] {}'.format(output_prefix['source'], res['source']))
    return res


def short_video_dl():
    """
    下载短视频为mp4格式

    Download short video as mp4

    :return:
    """
    from QuickStart_Rhy.NetTools.NormalDL import normal_dl
    from QuickStart_Rhy.ImageTools.VideoTools import tomp4
    from QuickStart_Rhy import remove
    res = short_video_info(son_call=True)

    print()
    if not res:
        print('Download failed' if user_lang != 'zh' else '下载失败')
        return
    normal_dl(res['video_url'], set_name=res['title'])
    tomp4(res['title'])
    remove(res['title'])


def acg():
    """
    获取随机acg图片链接（可选择下载）

    Get links to random ACG images (download optional)

    :return:
    """
    from QuickStart_Rhy.API.alapi import acg

    status, acg_link, width, height = acg()
    print("[%s] %s" % ('链接' if status else '错误', acg_link)) \
        if user_lang == 'zh' else \
        print("[%s] %s" % ('LINK' if status else 'ERROR', acg_link))
    if status:
        print('[尺寸]' if user_lang == 'zh' else '[SIZE]', width, '×', height)
        if 'save' in sys.argv[2:]:
            from QuickStart_Rhy.NetTools.NormalDL import normal_dl
            normal_dl(acg_link)
