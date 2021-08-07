# coding=utf-8
"""
调用各种qs的API

Call various QS API
"""
import sys
from . import user_lang, system, qs_default_console, qs_error_string, qs_info_string, qs_warning_string, requirePackage


def remove_bg():
    """
    删除图片背景

    Delete image background
    """
    try:
        path = sys.argv[2]
    except IndexError:
        qs_default_console.log(qs_error_string,
                               '%s: qs rmbg <%s>' % (('Usage', 'picture') if user_lang != 'zh' else ('用法', '图像')))
        return
    else:
        if path == '-helpF':
            qs_default_console.print(qs_info_string,
                                     '%s: qs rmbg <%s>' % (('Usage', 'picture')
                                                           if user_lang != 'zh' else ('用法', '图像')))
            return
        from .API.SimpleAPI import rmbg
        with qs_default_console.status('Dealing..' if user_lang != 'zh' else '处理中..') as st:
            rmbg(path)
            st.update(status='Done')


def smms():
    """
    上传图片或Markdown中图片到smms

    Upload images or Markdown images to SMMS
    """
    try:
        path = sys.argv[2]
    except IndexError:
        qs_default_console.log(
            qs_error_string,
            '%s: qs smms <%s>' % (('Usage', 'picture | *.md')
                                  if user_lang != 'zh' else ('用法', '图像 | *.md'))
        )
        return
    else:
        if path == '-help':
            qs_default_console.print(
                qs_info_string,
                '%s: qs smms <%s>' % (('Usage', 'picture | *.md')
                                      if user_lang != 'zh' else ('用法', '图像 | *.md'))
            )
            return
        from .API.SimpleAPI import smms
        with qs_default_console.status('Dealing..' if user_lang != 'zh' else '处理中..') as st:
            smms(path)
            st.update(status='Done')


def up_img():
    """
    上传图片或Markdown中图片到多平台（不保证数据安全）

    Upload images or Markdown images to multiple platforms (data security is not guaranteed)
    """

    def showSptPlatform(dt, ls):
        from rich.table import Table
        from rich.box import SIMPLE

        tb = Table('1', '2', '3', show_header=False, show_edge=False, box=SIMPLE)
        for indx in range(0, len(ls), 3):
            row = []
            for i in range(indx, indx + 3):
                if i < len(ls):
                    row.append(f'{ls[i]}: {dt[ls[i]]}')
                else:
                    break
            tb.add_row(*row)
        qs_default_console.print(
            qs_info_string,
            'Usage: qs upimg <picture | *.md> [platform]\n\nSupport ([platform]: description):'
            if user_lang != 'zh' else '用法: qs -upimg <图像 | *.md> [平台]\n\n支持 ([可选平台]: 描述):')
        qs_default_console.print(tb, justify="center")

    try:
        path = sys.argv[2]
    except IndexError:
        qs_default_console.log(qs_error_string, '%s: qs upimg <%s>' % (('Usage', 'picture | *.md')
                                                                       if user_lang != 'zh' else ('用法', '图像 | *.md')))
        return
    else:
        from .API.alapi import upload_image, _upimg_get_avaliable_platform
        import random

        spt_type = _upimg_get_avaliable_platform()
        spt_type_keys = list(spt_type.keys())
        if '-h' in sys.argv or '-help' in sys.argv:
            showSptPlatform(spt_type, spt_type_keys)
            qs_default_console.print(
                qs_info_string,
                'If you do not set platform, qs will randomly choose one.' if user_lang != 'zh' else
                '如果你没有设置平台，qs将随机抽取一个可用平台')
            return
        argv_len_3 = len(sys.argv) > 3
        if argv_len_3:
            sys.argv[3] = sys.argv[3].lower()
            type_map = {}
            for i in spt_type:
                type_map[i.lower()] = i

            upload_image(path, type_map[sys.argv[3]]) \
                if argv_len_3 and sys.argv[3] in type_map else (
                qs_default_console.print(
                    qs_warning_string,
                    ('No such platform: %s' if user_lang != 'zh' else '不支持设定的平台: %s') % sys.argv[3]),
                showSptPlatform(spt_type, spt_type_keys),
                qs_default_console.print(qs_error_string, 'Upload Failed' if user_lang != 'zh' else '上传失败!')
            )

        else:
            upload_image(path, plt_type=random.choice(spt_type_keys))


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
        qs_default_console.print(
            qs_info_string,
            'qs alioss:\n'
            '    -up <file> [bucket]: upload file to bucket\n'
            '    -dl <file> [bucket]: download file from bucket\n'
            '    -rm <file> [bucket]: remove file in bucket\n'
            '    -ls [bucket]       : get file info of bucket'
        ) if user_lang != 'zh' else qs_default_console.print(
            qs_info_string,
            'qs alioss:\n'
            '    -up <文件> [桶]: 上传文件至桶\n'
            '    -dl <文件> [桶]: 从桶下载文件\n'
            '    -rm <文件> [桶]: 从桶删除文件\n'
            '    -ls [桶]       : 获取桶文件信息'
        )
        return
    else:
        from .API.AliCloud import AliyunOSS
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
        qs_default_console.print(
            qs_info_string,
            'qs qiniu:\n'
            '    -up <file> [bucket]: upload file to bucket\n'
            '    -dl <file> [bucket]: download file from bucket\n'
            '    -cp <url > [bucket]: copy file from url\n'
            '    -rm <file> [bucket]: remove file in bucket\n'
            '    -ls [bucket]       : get file info of bucket'
        ) if user_lang != 'zh' else qs_default_console.print(
            qs_info_string,
            'qs qiniu:\n'
            '    -up <文件> [桶]: 上传文件至桶\n'
            '    -dl <文件> [桶]: 从桶下载文件\n'
            '    -cp <链接> [桶]: 从链接下载文件到桶\n'
            '    -rm <文件> [桶]: 从桶删除文件\n'
            '    -ls [桶]       : 获取桶文件信息'
        )
        return
    else:
        from .API.QiniuOSS import QiniuOSS
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
        qs_default_console.print(
            qs_info_string,
            'qs alioss:\n'
            '    -up <file> [bucket]: upload file to bucket\n'
            '    -dl <file> [bucket]: download file from bucket\n'
            '    -rm <file> [bucket]: remove file in bucket\n'
            '    -ls [bucket]       : get file info of bucket'
        ) if user_lang != 'zh' else qs_default_console.print(
            qs_info_string,
            'qs alioss:\n'
            '    -up <文件> [桶]: 上传文件至桶\n'
            '    -dl <文件> [桶]: 从桶下载文件\n'
            '    -rm <文件> [桶]: 从桶删除文件\n'
            '    -ls [桶]       : 获取桶文件信息'
        )
        return
    else:
        from .API.TencentCloud import TxCOS
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
    from . import trans_engine
    pyperclip = requirePackage('pyperclip')
    if trans_engine != 'default':
        from .API.TencentCloud import translate
    else:
        from .API.alapi import translate

    content = ' '.join(sys.argv[2:])
    if not content:
        try:
            content = pyperclip.paste()
        except:
            from . import qs_default_input
            content = qs_default_input.ask(
                'Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: '
                if user_lang != 'zh' else '抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:')
    if content:
        ret = translate(content.replace('\n', ' '))
        qs_default_console.print(ret) if ret else qs_default_console.log(qs_error_string, 'Translate Failed!')
    else:
        qs_default_console.log(
            qs_warning_string,
            "No content in your clipboard or command parameters!"
            if user_lang != 'zh' else
            '剪贴板或命令参数没有内容!')


def weather():
    """查天气 | Check weather"""
    from . import headers, dir_char
    from .ThreadTools import ThreadFunctionWrapper
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
    with qs_default_console.status('Requesting..' if user_lang != 'zh' else '请求中..') as st:
        for i in tls:
            i.join()
        st.update(status='Done')
    simple = tls[0].get_res()
    table = tls[1].get_res()
    if simple:
        if not loc:
            if user_lang == 'zh':
                from .API.alapi import translate
                enLocation = simple[0].split('：')[-1].strip()
                trans_loaction = translate(enLocation)
                qs_default_console.print('地区：' + trans_loaction if trans_loaction else enLocation)
            else:
                qs_default_console.print('Location' + simple[0][simple[0].index(':'):])
        simple = simple[2:7]
        print('\n'.join(simple))
    else:
        qs_default_console.log(qs_error_string, 'Get data failed.' if user_lang != 'zh' else '错误: 获取数据失败')
    if table:
        qs_default_console.print(table[3][:-1])
        bottom_line = 7
        try:
            while '╂' not in table[bottom_line]:
                bottom_line += 1
        except IndexError:
            qs_default_console.log(qs_error_string, 'Get Weather Data failed!' if user_lang != 'zh' else '获取天气数据失败')
            return
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
    from .API.IpInfo import get_ip_info
    return get_ip_info(ip)


def largeImage():
    """
    百度图片效果增强

    Baidu picture effect enhancement
    """
    try:
        path = sys.argv[2]
    except IndexError:
        qs_default_console.log(qs_error_string, '%s: qs LG <img>' % 'Usage' if user_lang != 'zh' else '用法')
        return
    else:
        from .API.BaiduCloud import ImageDeal
        aip_cli = ImageDeal()
        with qs_default_console.status('Dealing..' if user_lang != 'zh' else '处理中..') as st:
            aip_cli.largeImage(path, st)
            st.update(status='Done')


def AipNLP():
    """百度NLP | Baidu NLP"""
    from .API.BaiduCloud import AipNLP
    pyperclip = requirePackage('pyperclip')
    ct = sys.argv[2:]
    if not ct:
        try:
            ct = [pyperclip.paste()]
        except:
            from . import qs_default_input
            ct = [qs_default_input.ask(
                'Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: '
                if user_lang != 'zh' else '抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:')]
    NLP = AipNLP()
    for _id, line in enumerate(ct):
        ct[_id] = NLP.get_res(line)
        if _id == 9:
            qs_default_console.print('...')
        elif _id < 9:
            qs_default_console.print(ct[_id])
    try:
        pyperclip.copy('\n'.join(ct))
    except:
        pass


def CommonClipboard():
    """共享粘贴板"""
    from .API.CommonClipboard import CommonClipboard
    try:
        method = sys.argv[2]
        if method == 'get':
            CommonClipboard().get_msg()
        elif method == 'post':
            msg = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else None
            CommonClipboard().post_msg(msg) if msg else CommonClipboard().post_msg()
    except IndexError:
        qs_default_console.log(
            qs_error_string, "Usage:\n  1. qs cb <get>\n  2. qs cb <post> [msg]"
            if user_lang != 'zh' else '用法:\n  1. qs cb <get>\n  2. qs cb <post> [消息]')
        return


def Pasteme():
    """Pasteme信息传递"""
    from .API.SimpleAPI import pasteme
    try:
        method = sys.argv[2]
        key = sys.argv[3]
        password = sys.argv[4] if len(sys.argv) > 4 else ''
        pasteme(key, password, method)
    except IndexError:
        qs_default_console.log(
            qs_error_string, "Usage:\n  1. qs pasteme <get> <key> [password]\n  2. qs pasteme <post> <lang> [password]"
            if user_lang != 'zh' else "用法:\n  1. qs pasteme <get> <键值> [密码]\n  2. qs pasteme <post> <语言> [密码]")
        return


def bili_cover():
    """下载Bilibili视频、直播的封面图片（视频链接、视频号均可识别）"""
    from .API.alapi import bili_cover as bc
    pyperclip = requirePackage('pyperclip')

    try:
        url = sys.argv[2]
    except IndexError:
        try:
            url = pyperclip.paste()
        except:
            qs_default_console.log(
                qs_error_string, 'Sorry, but your system may not be suppported by `pyperclip`'
                if user_lang != 'zh' else '抱歉，但是“pyperclip”不支持你的系统')
            return
    if not url:
        qs_default_console.log(
            qs_error_string, 'Usage: qs bcv <url | video code>'
            if user_lang != 'zh' else '用法: qs bcv <链接 | 视频码>')
        return
    bc(url)


def gbc():
    """查询中国垃圾分类（且仅支持中文查询）"""
    from .API.alapi import garbage_classification
    try:
        with qs_default_console.status('Requesting data..' if user_lang != 'zh' else '请求数据中..') as st:
            res = garbage_classification(sys.argv[2:])
            st.update(status='Done')
        qs_default_console.print(res, justify='center')
    except Exception as e:
        qs_default_console.print(qs_error_string, repr(e))
        qs_default_console.print(
            qs_error_string,
            'Usage: qs gbc <garbage...>' if user_lang != 'zh' else '用法: qs gbc <垃圾...>')


def short_video_info(son_call=False):
    """
    获取短视频信息 | Get short video information

    :return:
    """
    from .API.alapi import short_video_info
    from .NetTools import get_fileinfo, size_format
    pyperclip = requirePackage('pyperclip')
    import re
    try:
        url = sys.argv[2]
    except IndexError:
        try:
            url = pyperclip.paste()
            url = re.findall('https?://(?:[-\w.]|%[\da-fA-F]{2}|[/])+', url)[0]
        except:
            qs_default_console.print(
                qs_error_string, 'Sorry, but your system may not be suppported by `pyperclip`'
                if user_lang != 'zh' else '抱歉，但是“pyperclip”不支持你的系统')
            return
    if not url:
        qs_default_console.print(
            qs_error_string, 'Usage: qs svi <url/video code>' if not son_call else 'Usage: qs svd <url/video code>')
        return
    output_prefix = {
        'title': 'Title ' if user_lang != 'zh' else '标题',
        'video': 'Video ' if user_lang != 'zh' else '视频',
        'cover': 'Cover ' if user_lang != 'zh' else '封面',
        'source': 'Source' if user_lang != 'zh' else '来源'
    }
    status, res = short_video_info(url.strip('/'))
    if not status:
        qs_default_console.print(qs_info_string, res['title'] + ':' + res['source'])
        return status
    showStatus = '-url' in sys.argv
    qs_default_console.print(qs_info_string, '[{}] {}'.format(output_prefix['title'], res['title']))
    if res['video_url']:
        sz = int(get_fileinfo(res['video_url'])[-1].headers['content-length']) if not son_call else -1
        qs_default_console.print(
            qs_info_string,
            '[{}] {}\n{}'.format(
                output_prefix['video'],
                size_format(sz, True) if sz > 0 else '--',
                res['video_url'] if showStatus else ''
            )
        )
    if showStatus:
        sz = int(get_fileinfo(res['cover_url'])[-1].headers['content-length'])
        qs_default_console.print(
            qs_info_string,
            '[{}] {}\n{}'.format(output_prefix['cover'], size_format(sz, True), res['cover_url'] if showStatus else '')
        )
    if system == 'darwin':
        from .ImageTools.ImagePreview import image_preview
        image_preview(res['cover_url'], True)
    if 'source' in res and res['source']:
        qs_default_console.print(qs_info_string, '[{}] {}'.format(output_prefix['source'], res['source']))
    return res


def short_video_dl():
    """
    下载短视频为mp4格式

    Download short video as mp4

    :return:
    """
    from .NetTools.NormalDL import normal_dl
    from .ImageTools.VideoTools import tomp4
    from . import remove
    res = short_video_info(son_call=True)

    if not res:
        qs_default_console.print(qs_error_string, 'Download failed' if user_lang != 'zh' else '下载失败')
        return

    fileName = res['title'] if res['title'] else 'UnknownTitle'
    if res['video_url']:
        normal_dl(res['video_url'], set_name=fileName)
        tomp4(fileName)
        remove(fileName)
    elif 'pics' in res:
        from .ImageTools.ImageTools import topng
        for index, url in enumerate(res['pics']):
            normal_dl(url, set_name=fileName + str(index + 1))
            topng(fileName + str(index + 1))
            remove(fileName + str(index + 1))


def acg():
    """
    获取随机acg图片链接（可选择下载）

    Get links to random ACG images (download optional)

    :return:
    """
    import random
    from .API.alapi import acg
    from .API.SimpleAPI import acg2

    st = qs_default_console.status('Requesting data..' if user_lang != 'zh' else '请求数据中..')
    st.start()
    try:
        status, acg_link, width, height = random.choice([acg, acg2])()
        qs_default_console.print(qs_info_string, f"{'链接' if user_lang == 'zh' else 'LINK'}: {acg_link}") \
            if status else qs_default_console.log(qs_error_string, acg_link)
        if status:
            qs_default_console.print(qs_info_string, '尺寸:' if user_lang == 'zh' else 'SIZE:', width, '×', height)
            if '-save' in sys.argv[2:]:
                from . import dir_char
                from .NetTools.NormalDL import normal_dl
                st.stop()
                acg_link = normal_dl(acg_link)  # disable download status for Windows
            if system == 'darwin':  # Only support iTerm for Mac OS X
                from .ImageTools.ImagePreview import image_preview
                st.update(status='Loading image...\n' if user_lang != 'zh' else '加载图片中..\n')
                image_preview(open(acg_link) if '-save' in sys.argv[2:] else acg_link,
                              '-save' not in sys.argv[2:], qs_console_status=st)
                return
    except Exception as e:
        qs_default_console.print(qs_error_string, repr(e))
    finally:
        st.stop()


def bingImg():
    """
    获取bing图片链接（可选择下载）

    Get links to bing images (download optional)

    :return:
    """
    from .API.alapi import bingImg

    st = qs_default_console.status('Requesting data..' if user_lang != 'zh' else '请求数据中..')
    st.start()

    try:
        status, acg_link, cprt = bingImg()
        qs_default_console.print(qs_info_string, f"{'链接' if user_lang == 'zh' else 'LINK'}: {acg_link}") \
            if status else qs_default_console.log(qs_error_string, acg_link)
        if status:
            qs_default_console.print(qs_info_string, '版权:' if user_lang == 'zh' else 'CPRT:', cprt)
            if '-save' in sys.argv[2:]:
                from .NetTools.NormalDL import normal_dl
                st.stop()
                acg_link = normal_dl(acg_link)
            if system == 'darwin':  # Only support iTerm for Mac OS X
                from .ImageTools.ImagePreview import image_preview
                st.update(status='Loading image...' if user_lang != 'zh' else '加载图片中..')
                image_preview(open(acg_link) if '-save' in sys.argv[2:] else acg_link,
                              '-save' not in sys.argv[2:], qs_console_status=st)
    except Exception as e:
        qs_default_console.print(qs_error_string, repr(e))
    finally:
        st.stop()


def preview_html_images():
    """
    获取网页中图片链接（可在Mac::iTerm中自动预览）

    Get links to pictures in the web page (automatically previewed in Mac::iTerm)

    :return:
    """
    from .API.SimpleAPI import imgs_in_url
    save_flag = '-save' in sys.argv
    if save_flag:
        sys.argv.remove('-save')
    for url in sys.argv[2:]:
        imgs_in_url(url, save_flag)


def kdCheck():
    """
    查国内快递

    Check domestic express

    :return:
    """
    from .API.alapi import kdCheck

    with qs_default_console.status('Requesting data..' if user_lang != 'zh' else '请求数据中..'):
        status, code, msg = kdCheck(sys.argv[2])
        if not status:
            qs_default_console.print(qs_error_string, msg)
            return

    from .TuiTools.Table import qs_default_table
    from . import table_cell
    from rich.text import Text

    width = qs_default_console.width // 4 * 3
    tb = qs_default_table(
        [
            {'header': "Time" if user_lang != 'zh' else '时间', 'justify': "center", 'style': "bold cyan"},
            {'header': "Description" if user_lang != 'zh' else '描述', 'justify': "center", 'no_wrap': False},
            {'header': "Status" if user_lang != 'zh' else '状态', 'justify': "center"},
        ], ([
                '[bold underline red]Unknown:heavy_exclamation_mark:', '[bold underline yellow]In transit:airplane:',
                '[bold underline green]In delivery:delivery_truck:', '[bold underline bold green]Signed receipt:hearts:'
            ][code] if user_lang != 'zh' else [
            '[bold underline red]未知:heavy_exclamation_mark:', '[bold underline yellow]运输中:airplane:',
            '[bold underline green]派送中:delivery_truck:', '[bold underline magenta]已签收:hearts:'
        ][code]) + '\n'
    )
    for info in msg[:-1] if code != 3 else msg:
        tb.add_row(
            info['time'], Text(table_cell(info['content'], width), justify='full')
            , '[green]:heavy_check_mark:'
        )
    if code != 3:
        tb.add_row(
            msg[-1]['time'], Text(table_cell(msg[-1]['content'], width), justify='full')
            , '[bold yellow]:arrow_left:'
        )
    qs_default_console.print(tb, justify="center")


def loli():
    """
    获取一张"可爱"萝莉图的URL，Mac+iTerm2下可在终端预览

    Get the URL of a "cute" Lori map, which can be previewed on the terminal under MAC + iterm2

    :return:
    """
    from .API.Lolicon import loli_img
    from .ImageTools import ImagePreview
    from .NetTools import NormalDL

    with qs_default_console.status('Requesting data..' if user_lang != 'zh' else '请求数据中..'):
        status, msg, data = loli_img()
        if not status:
            qs_default_console.print(qs_error_string, msg)
            return

    save_flag = '-save' in sys.argv
    proxy = ''

    if '-p' in sys.argv:
        from . import qs_config
        proxy = qs_config.basicSelect('default_proxy')

    for img in data:
        qs_default_console.print(f'[bold underline]{img["title"]} [dim]{img["author"]}', justify="center")
        qs_default_console.print(qs_info_string, '[bold]link' if user_lang != 'zh' else '[bold]链接', img['url'])
        qs_default_console.print(qs_info_string, '[bold]size' if user_lang != 'zh' else '[bold]尺寸',
                                 img['width'], 'x', img['height'])
        if save_flag:
            img['url'] = NormalDL.normal_dl(img['url'], set_proxy=proxy, set_referer='https://i.pximg.net')
        if system == 'darwin':
            ImagePreview.image_preview(open(img['url']) if save_flag else img['url'], not save_flag
                                       , set_proxy=proxy, set_referer='https://i.pximg.net')

        qs_default_console.print('-' * (qs_default_console.width // 4 * 3), justify='center')


def pinyin():
    from .API.alapi import pinyin

    content = ' '.join(sys.argv[2:])
    if not content:
        try:
            pyperclip = requirePackage('pyperclip')
            content = pyperclip.paste()
        except:
            from . import qs_default_input
            content = qs_default_input.ask(
                'Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: '
                if user_lang != 'zh' else '抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:')
    with qs_default_console.status('Requesting data..' if user_lang != 'zh' else '请求数据中..') as st:
        status, res = pinyin(content)
        st.update(status='Done' if user_lang != 'zh' else '请求完成')
    qs_default_console.print(qs_info_string, content)
    qs_default_console.print(qs_info_string if status else qs_error_string, res)


def photo():
    from .API.SimpleAPI import photo

    st = qs_default_console.status('Requesting data..' if user_lang != 'zh' else '请求数据中..')
    st.start()

    try:
        status, acg_link, name = photo()
        qs_default_console.print(qs_info_string, f"{'链接' if user_lang == 'zh' else 'LINK'}: {acg_link}") \
            if status else qs_default_console.log(qs_error_string, acg_link)
        if status:
            if '-save' in sys.argv[2:]:
                from .NetTools.NormalDL import normal_dl
                st.stop()
                acg_link = normal_dl(acg_link)
            if system == 'darwin':  # Only support iTerm for Mac OS X
                from .ImageTools.ImagePreview import image_preview
                st.update(status='Loading image...' if user_lang != 'zh' else '加载图片中..')
                image_preview(open(acg_link) if '-save' in sys.argv[2:] else acg_link,
                              '-save' not in sys.argv[2:], qs_console_status=st)
    except Exception as e:
        qs_default_console.print(qs_error_string, repr(e))
    finally:
        st.stop()


def setu():
    import random
    random.choice([acg, loli, photo])()


def exchange():
    from .API.alapi import exchange

    st = qs_default_console.status('Requesting data..' if user_lang != 'zh' else '请求数据中..')
    st.start()
    try:
        status, data = exchange(sys.argv[3], float(sys.argv[2]))
        qs_default_console.print(f"{sys.argv[2]} {sys.argv[3]} ==> {data['exchange']} × {sys.argv[2]} = "
                                 f"{data['exchange_round']} {data['currency_to']}\n"
                                 f"{'Update' if user_lang != 'zh' else '更新时间'}: {data['update_time']}",
                                 justify="center") \
            if status else qs_default_console.log(qs_error_string, data)
    except Exception as e:
        qs_default_console.print(qs_error_string, repr(e))
    finally:
        st.stop()


def zhihuDaily():
    from .API.alapi import zhihuDaily
    from rich.panel import Panel

    st = qs_default_console.status('Requesting data..' if user_lang != 'zh' else '请求数据中..')
    st.start()
    try:
        status, data = zhihuDaily()
        st.stop()
        if not status:
            qs_default_console.log(qs_error_string, data)
            return
        data = data['stories'] + data['top_stories']
        for item in data:
            res = '[bold cyan]' + ('Author: ' if user_lang != 'zh' else '作者: ')
            res += '[bold white]' + item['hint'] + '[/bold white]\n'
            res += '[bold cyan]' + ('Link:' if user_lang != 'zh' else '链接: ')
            res += '[bold blue]' + item['url'] + '[/bold blue]\n'
            res += '[bold cyan]' + ('Image: \n' if user_lang != 'zh' else '图像: \n')
            if 'images' in item:
                res += '[bold blue]  ' + '\n  '.join(item['images'])
            elif 'image' in item:
                res += '[bold blue]  ' + item['image']
            qs_default_console.print(Panel(res, title='[b]' + item['title']), justify="center", end='/n/n')
    except Exception as e:
        qs_default_console.print(qs_error_string, repr(e))
    finally:
        st.stop()


def wallhaven():
    from .API.SimpleAPI import wallhaven

    url, oneFlag = '', False
    if '-h' in sys.argv:
        return qs_default_console.print(qs_info_string, "Usage: qs wallhaven [-u <url>] [-one] [-save]")

    if '-u' in sys.argv:
        url = sys.argv[sys.argv.index('-u') + 1]
        sys.argv.remove('-u')
        sys.argv.remove(url)

    oneFlag = '-one' in sys.argv

    res = wallhaven(randomOne=oneFlag) if not url else wallhaven(url, randomOne=oneFlag)
    if not res:
        return

    if '-save' in sys.argv:
        from .NetTools.NormalDL import normal_dl
        import os
        for i in res:
            name = i['url'].split('/')[-1]
            if os.path.exists(name):
                qs_default_console.print(qs_warning_string,
                                         f'{name} is exists!' if user_lang != 'zh' else f'{name} 已存在!')
                continue
            qs_default_console.print(qs_info_string, f"Deal:\t{name}")
            qs_default_console.print(qs_info_string, f'Size:\t{" × ".join([str(j) for j in i["size"]])}')
            normal_dl(i['url'], output_error=True, failed2exit=True)
            qs_default_console.print('-' * qs_default_console.width)
    else:
        if oneFlag:
            res = res[0]
            qs_default_console.print(qs_info_string, 'URL:\t', res['url'])
            qs_default_console.print(qs_info_string, 'SIZE:\t', ' × '.join([str(i) for i in res['size']]))
            from .ImageTools.ImagePreview import image_preview

            with qs_default_console.status('Getting..' if user_lang != 'zh' else '获取图片中..') as st:
                image_preview(res['url'], True, qs_console_status=st)
        else:
            from .TuiTools.Table import qs_default_table

            tb = qs_default_table([
                {'header': "ID" if user_lang != 'zh' else '编号', 'justify': "center", 'style': "bold"},
                {'header': 'URL', 'justify': "center", 'style': "bold cyan"},
                {'header': 'Size' if user_lang != 'zh' else '尺寸', 'justify': "center"}
            ], 'Wallhaven Anime TopList\n')
            for iid, item in enumerate(res):
                tb.add_row(str(iid), item['url'], ' × '.join([str(i) for i in item['size']]))
            qs_default_console.print(tb, justify="center")


def lmgtfy():
    from .API.SimpleAPI import lmgtfy
    pyperclip = requirePackage('pyperclip')

    keyword = ' '.join(sys.argv[2:])
    res = lmgtfy(keyword)
    try:
        pyperclip.copy(res)
        qs_default_console.print(
            qs_info_string,
            'The generated link has been copied for you, and teach your friends how to use Google! (Can also Copy '
            'Following link'
            if user_lang != 'zh' else '已经为您复制生成的链接，快教朋友如何使用Google吧! (也可以复制下面的链接)'
        )
    except:
        qs_default_console.print(
            qs_warning_string,
            'Failed to use clipboard, you can copy the flowing link:'
            if user_lang != 'zh' else '调用剪切板失败，你可以复制下面的链接:'
        )
    qs_default_console.print(qs_info_string, res)


def daily60s():
    from .API.alapi import daily60s

    status, res = daily60s()
    if not status:
        return qs_default_console.print(qs_error_string, res)

    from rich.padding import Padding
    import signal
    import time

    cur_index = 0

    with qs_default_console.status('showing' if user_lang != 'zh' else '展示中') as st:
        def dealSignal(*argv):
            for index in range(cur_index + 1, len(res['news'])):
                qs_default_console.print(Padding(res['news'][index], (0, int(0.2 * qs_default_console.width))))
                qs_default_console.print()
            qs_default_console.print('-' * qs_default_console.width)
            qs_default_console.print(res['weiyu'] + '\n', justify='center')

            if '-save' in sys.argv:
                import os
                from .NetTools.NormalDL import normal_dl

                st.stop()
                name = normal_dl(res['image'], set_name='news.png')
                st.start()
                if system == 'darwin':
                    qs_default_console.print('Preview' if user_lang != 'zh' else '预览', justify='center')
                    from .ImageTools.ImagePreview import image_preview

                    st.update(status='loading image..' if user_lang != 'zh' else '加载图片中..')
                    image_preview(open(name), qs_console_status=st)
            exit(0)

        signal.signal(signal.SIGINT, dealSignal)
        qs_default_console.print('[bold magenta underline]每天60秒读懂世界[/bold magenta underline]', justify='center')
        qs_default_console.print(res['date'], justify='center')
        qs_default_console.print('-' * qs_default_console.width)
        len_ls = [len(i) for i in res['news']]
        total_len = sum(len_ls)
        len_ls = [i / total_len * 60 for i in len_ls]
        len_ls[-1] = 0

        for index, item in enumerate(res['news']):
            qs_default_console.print(Padding(item, (0, int(0.2 * qs_default_console.width))))
            qs_default_console.print()
            cur_index = index
            time.sleep(len_ls[index])
    dealSignal()
