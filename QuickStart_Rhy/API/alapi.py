# coding=utf-8
from . import *
from .. import user_currency
import os
import json
from urllib.parse import quote
import requests

__common_token__ = 'hUxPTdnybk1XLUEFtzkj'
alapi_token = pre_check('alapi_token', False)
if not alapi_token:
    from .. import qs_default_console, qs_error_string, qs_warning_string
    from PyInquirer import prompt

    qs_default_console.print(qs_error_string, 'This function require alapi token!\n这个功能需要alapi token\n')
    if prompt({
        'type': 'confirm',
        'name': 'confirm',
        'message': 'To get alapi token?\n是否前往获取alapi token?',
        'default': True
    })['confirm']:
        from .. import u
        from .. import qs_config

        try:
            u(['https://www.alapi.cn/'])
        except Exception as e:
            qs_default_console.print(qs_error_string, 'Failed to open browser, try url: https://www.alapi.cn/')
        finally:
            alapi_token = prompt({
                'type': 'input',
                'name': 'token',
                'message': 'Input alapi token | 输入alapi token:',
            })['token']
            qs_config.apiUpdate('alapi_token', alapi_token)
    elif prompt({
        'type': 'confirm',
        'name': 'confirm',
        'message': 'Use common but limited token?\n是否愿意使用公共但是受限的token?',
        'default': True
    })['confirm']:
        alapi_token = __common_token__
        qs_config.apiUpdate('alapi_token', alapi_token)
        qs_default_console.print(
            qs_warning_string,
            'Tokens with restricted applications may not be able to use the functions provided by alapi normally, '
            'and you can try again multiple times.'
            if user_lang != 'zh' else '应用受限的token可能无法正常使用alapi提供的功能，可多次重新尝试。')
    else:
        exit()

if not pre_check('__ban_warning', False) and alapi_token == __common_token__:
    from .. import qs_default_console, qs_warning_string
    qs_default_console.print(
        qs_warning_string, 'Using common but limited token.' if user_lang != 'zh' else '正在使用公共但受限的token')
    qs_default_console.print(
        qs_warning_string,
        'If you do not want this, try to apply one:' if user_lang != 'zh' else '如果您不想这样, 可以来申请一个自己的:',
        'https://www.alapi.cn/')

v2_url = "https://v2.alapi.cn/api/"


def _upimg_get_avaliable_platform():
    json_string = requests.get(v2_url + 'image/type', headers={'token': alapi_token}).text
    return json.loads(json_string)['data']


def upload_image(file_path: str, plt_type: str = ''):
    """
    上传图片或Markdown中所有的图片到多平台（免API KEY，但不保证数据安全）

    Upload images or all images from Markdown to multiple platforms (API-free KEY, but data security is not guaranteed)

    :param file_path: 图片或Markdown文件路径
    :param plt_type: 平台（使用 qs -upload_image -help查看支持的平台）
    :param set_url: {v1_url} or {v2_url} 默认 v1
    :return: None
    """
    from .. import qs_default_console, qs_error_string, qs_info_string, qs_warning_string
    from ..TuiTools.Table import qs_default_table

    set_url = v2_url
    res_table = qs_default_table([
        {'header': "File" if user_lang != 'zh' else '文件', 'no_wrap': True, 'justify': "center", 'style': "bold cyan"},
        {'header': "Status" if user_lang != 'zh' else '状态', 'no_wrap': True, 'justify': "center"},
        {'header': "Url" if user_lang != 'zh' else '链接', 'no_wrap': True, 'justify': "center"},
    ])

    def post_img(path):
        if not os.path.exists(path):
            return False
        try:
            data = {'type': plt_type}
            file = [('image', open(path, 'rb'))]
        except:
            return False
        if plt_type:
            res_json = requests.post(set_url + 'image', data=data, files=file).text \
                if not alapi_token else \
                requests.post(set_url + 'image', data=data, files=file, headers={'token': alapi_token}).text
        else:
            res_json = requests.post(set_url + 'image', files=file).text \
                if not alapi_token else \
                requests.post(set_url + 'image', files=file, headers={'token': alapi_token}).text
        try:
            return json.loads(res_json)
        except Exception as e:
            qs_default_console.print(qs_error_string, repr(e), res_json)
            return False

    def get_path(rt, rel):
        return os.path.abspath(rt + rel)

    def format_markdown(path):
        import re
        from rich.progress import Progress
        from .. import user_root
        rt_path = dir_char.join(os.path.abspath(path).split(dir_char)[:-1]) + dir_char
        img_dict = {}
        with open(path, 'r') as fp:
            ct = fp.read()
        aims = re.findall('!\[.*?]\((.*?)\)', ct, re.M) + re.findall('<img.*?src="(.*?)".*?>', ct, re.M)
        progress = Progress(console=qs_default_console)
        pid = progress.add_task('  Upload' if user_lang != 'zh' else '  上传', total=len(aims))
        progress.start()
        progress.start_task(pid)
        for aim in aims:
            if aim.startswith('http'):  # Uploaded
                qs_default_console.print(qs_warning_string, aim,
                                         'is not a local file' if user_lang != 'zh' else '非本地文件')
                progress.advance(pid, 1)
                continue
            raw_path = aim
            aim = aim.replace('~', user_root)
            aim = aim if aim.startswith(dir_char) else get_path(rt_path, aim)
            if aim not in img_dict:
                qs_default_console.print(qs_info_string, 'Start uploading:' if user_lang != 'zh' else '正在上传:', aim)
                res_dict = post_img(aim)
                if not res_dict:
                    res_table.add_row(aim.split(dir_char)[-1], 'No File' if user_lang != 'zh' else '无文件', '')
                    img_dict[aim] = False
                else:
                    try:
                        res_table.add_row(
                            aim.split(dir_char)[-1], str(res_dict['code']),
                            res_dict['msg'] if res_dict['code'] != 200 else (
                                res_dict['data']['url']
                                if res_dict['data']['url'] else plt_type + ' failed')
                        )
                        img_dict[aim] = res_dict['data']['url'] if res_dict['code'] == 200 else False
                    except Exception:
                        qs_default_console.print(qs_error_string, res_dict)
                        res_table.add_row(aim.split(dir_char)[-1], str(res_dict['code']), res_dict['msg'])
                        img_dict[aim] = False

                if img_dict[aim]:
                    qs_default_console.print(qs_info_string, 'replacing img:' if user_lang != 'zh' else '替换路径',
                                             f'"{raw_path}" with "{img_dict[aim]}"')
                    ct = ct.replace(raw_path, img_dict[aim])
            progress.advance(pid, 1)
        progress.stop()
        with open(path, 'w') as fp:
            fp.write(ct)
        qs_default_console.print(res_table, justify="center")

    try:
        is_md = file_path.endswith('.md')
    except IndexError:
        qs_default_console.print(
            qs_error_string, 'Usage: qs -upimg {*.md} | {picture}'
            if user_lang != 'zh' else '使用: qs -upimg {Markdown文件} 或 {任意图片文件}')
    else:
        if is_md:
            format_markdown(file_path)
        else:
            res = post_img(file_path)
            if not res:
                res_table.add_row(os.path.basename(file_path), 'No File', '')
            else:
                try:
                    res_table.add_row(
                        os.path.basename(file_path), str(res['code']),
                        res['msg'] if res['code'] != 200 else res['data']['url']
                    )
                except Exception:
                    res_table.add_row(os.path.basename(file_path), str(res['code']), res['msg'])
            qs_default_console.print(res_table, justify="center")


def translate(text: str, from_lang: str = 'auto', to_lang: str = user_lang):
    """
    获取翻译结果

    Get the translation results.
    
    :param text: 待翻译内容 | Content to be translated.
    :param from_lang: 语种来源 | Source language
    :param to_lang: 翻译成的语种 | Translated into the language
    :return: 翻译的文本 | Translated text
    """
    global alapi_token
    try:
        request_info = 'q={}&from={}&to={}'.format(quote(text, 'utf-8'), from_lang, to_lang) if from_lang \
            else 'q={}&to={}'.format(quote(text, 'utf-8'), to_lang)
        res = requests.post(v2_url + 'fanyi', data=request_info,
                            headers={'Content-Type': "application/x-www-form-urlencoded", 'token': alapi_token}
                            if alapi_token else {'Content-Type': 'application/x-www-form-urlencoded'})
        if res.status_code == requests.codes.ok:
            res = json.loads(res.text)
            if res['code'] != 200:
                return "[ERROR] {}".format(res['msg'])
            return res['data']['dst']
        return "[ERROR] 未知错误 | Unknown Error"
    except Exception as e:
        return f"[ERROR] {repr(e)}"


def bili_cover(url: str):
    """
    获取BiliBili视频封面

    Get the BiliBili video cover

    :param url: BiliBili视频链接或视频号 | BiliBili video link or video number
    :return:
    """
    import re
    from ..NetTools.NormalDL import normal_dl
    from .. import qs_default_console, qs_error_string, qs_info_string
    try:
        res = requests.post(v2_url + 'bilibili/cover', data='c=' + url,
                            headers={'Content-Type': 'application/x-www-form-urlencoded', 'token': alapi_token})
    except Exception as e:
        return qs_default_console.print(qs_error_string, repr(e))
    if res.status_code == requests.codes.ok:
        res = json.loads(res.text)
        if res['code'] != 200 or res['msg'] != 'success':
            qs_default_console.log(
                qs_error_string, ("Get cover with: %s failed:" if user_lang != 'zh' else '下载封面: %s 失败: ') % url)
            return
        res = res['data']
        res['description'] = res['description'].replace('<br />', '\n\t')
        res['description'] = res['description'].replace('&nbsp;', ' ')
        res['description'] = re.sub('<.*?>', '', res['description']).strip()  # 忽略HTML标签
        qs_default_console.print(qs_info_string, 'TITLE:' if user_lang != 'zh' else '标题:', '%s' % res['title'])
        qs_default_console.print(qs_info_string, '' if user_lang != 'zh' else '简介:', end='\n\t')
        qs_default_console.print(res['description'], end='\n\n')
        normal_dl(res['cover'], res['title'] + '.' + res['cover'].split('.')[-1])
        if system == 'darwin':
            from ..ImageTools.ImagePreview import image_preview
            from PIL import Image
            image_preview(Image.open(res['title'] + '.' + res['cover'].split('.')[-1]))
    else:
        qs_default_console.log(qs_error_string,
                               f"Get cover with: {url} failed" if user_lang != 'zh' else f'下载封面: {url} 失败')


def ip_info(ip: str):
    """
    获取ip的运营商、地理位置等数据

    Get IP operator, geographic location and other data

    :param ip: ipv4, ipv6, empty means current machine
    :return: data dict {ip, isp, pos | ERROR MESSAGE, location | ERROR code}
    """
    try:
        res = requests.get(v2_url + ('ip?ip=%s&format=json' % ip if ip else 'ip') , headers={'token': alapi_token})
        res = json.loads(res.text)
        if res['code'] != 200:
            return {'ip': ip, 'isp': '', 'pos': res['msg'], 'location': '{code, %s}' % res['code']}
        return res['data']
    except Exception as e:
        return {'ip': ip, 'isp': '', 'pos': 'Network Error'
                if user_lang != 'zh' else '网络错误', 'location': '{code, %s}' % repr(e)}


def garbage_classification(query_ls: list):
    """
    查询中国垃圾分类

    Search Chinese garbage classification

    :param query_ls: 待查询的垃圾列表 | garbage list
    :return: 查询结果的字符串表格 | string table
    """
    from .. import qs_default_console, cut_string
    width = qs_default_console.width // 5 * 2 - 1

    def fmt_string(string, pre_num):
        return '\n' * pre_num + ' '.join(cut_string(string, width))

    from ..TuiTools.Table import qs_default_table
    from rich.text import Text
    import math

    table = qs_default_table([
        {'header': '名称', 'justify': 'center', 'style': 'bold cyan'},
        {'header': '分类', 'justify': 'center'},
        {'header': '解释', 'justify': 'center'},
        {'header': '提示', 'justify': 'center'},
    ], '[bold underline] 查询结果\n')
    first_flag = True
    for query_el in query_ls:
        if first_flag:
            first_flag = False
        else:
            table.add_row(Text('-', style='none'), Text('-', style='none'), '-', '-')
        res = requests.post(v2_url + 'garbage',
                            data="name={}".format(quote(query_el, 'utf-8')),
                            headers={'Content-Type': "application/x-www-form-urlencoded", 'token': alapi_token}
                            if alapi_token else {'Content-Type': 'application/x-www-form-urlencoded'})
        if res.status_code == requests.codes.ok:
            res = json.loads(res.text)
            if res['code'] != 200:
                table.add_row(fmt_string(query_el, 0), '', '', fmt_string(res['msg'], 0))
                continue
            try:
                res = res['data'][0]
                half_rows = [math.ceil(len(query_el) / width / 2), 1, math.ceil(len(res['explain']) / width / 2),
                             math.ceil(len(res['tip']) / width / 2)]
                max_row = max(half_rows)
                half_rows = [max_row - i for i in half_rows]
                table.add_row(
                    fmt_string(query_el, half_rows[0]),
                    fmt_string(
                        [
                            '[bold green]可回收', '[bold red]有害',
                            '[bold yellow]厨余(湿)', '[bold blue]其他(干)'
                        ][int(res['type']) - 1], half_rows[1]
                    ),
                    Text(fmt_string(res['explain'], half_rows[2]), justify='full'),
                    Text(fmt_string(res['tip'], half_rows[3]), justify='full')
                )
            except IndexError:
                table.add_row(fmt_string(query_el, 0), 'Unknown', '未知垃圾', '未知垃圾')
        else:
            table.add_row(fmt_string(query_el, 0), 'Unknown', 'None', 'Request Error')
    return table


def short_video_info(url: str):
    """
    解析多平台短视频，并返回视频信息与下载直链

    Parse multi - platform short video and return video information with download straight link

    :param url: 短视频分享链接 | Short video sharing link
    :return:
    """
    try:
        res = requests.post(v2_url + "video/url", data="url={}".format(quote(url, 'utf-8')),
                            headers={'Content-Type': "application/x-www-form-urlencoded", 'token': alapi_token}
                            if alapi_token else {'Content-Type': "application/x-www-form-urlencoded"})
        res = json.loads(res.text)
        if res['code'] != 200:
            return False, {'title': res['msg'], 'cover_url': 'None', 'video_url': 'None', 'source': str(res['code'])}
        return True, res['data']
    except:
        return False, {'title': '网络错误' if user_lang == 'zh' else 'Network Error',
                       'cover_url': 'None', 'video_url': 'None', 'source': 'Unknown'}


def acg():
    """
    随机获取一张acg图片链接

    Get a random link to an ACG image

    :return: acg image link
    """
    try:
        res = requests.post(v2_url + 'acg', data='format=json',
                            headers={'Content-Type': "application/x-www-form-urlencoded", 'token': alapi_token}
                            if alapi_token else {'Content-Type': "application/x-www-form-urlencoded"})
        res = json.loads(res.text)
        if res['code'] != 200:
            return False, res['msg'], 0, 0
        return True, res['data']['url'], res['data']['width'], res['data']['height']
    except Exception as e:
        return False, repr(e), 0, 0


def bingImg():
    """
    随机获取一张bing图片链接

    Get a link to a bing picture at random

    :return: image link
    """
    try:
        res = requests.post(v2_url + 'bing', data='format=json',
                            headers={'Content-Type': "application/x-www-form-urlencoded", 'token': alapi_token}
                            if alapi_token else {'Content-Type': "application/x-www-form-urlencoded"})
        res = json.loads(res.text)
        if res['code'] != 200:
            return False, res['msg'], ''
        return True, res['data']['url'], res['data']['copyright']
    except Exception as e:
        return False, repr(e), ''


def kdCheck(kd_number: str):
    """
    查询中国快递

    Inquire about China Express

    :param kd_number: 快递单号 | courier number
    :return: bool, list
    """
    try:
        res = requests.post(v2_url + 'kd', data="number=%s" % kd_number,
                            headers={'Content-Type': 'application/x-www-form-urlencoded', 'token': alapi_token})
        res = json.loads(res.text)
        if res['code'] != 200:
            return False, 0, res['msg']
        return True, (int(res['data']['status']) if 'status' in res['data'] else int(res['data']['state'])), \
               res['data']['info']
    except Exception as e:
        return False, 0, repr(e)


def pinyin(zh_str: str):
    """
    查询中文的拼音

    Query Chinese pinyin

    :param zh_str: Chinese | 中文
    :return:
    """
    try:
        res = requests.post(v2_url + 'pinyin', data=f'word={quote(zh_str, "utf-8")}&tone=1&abbr=0',
                            headers={'Content-Type': 'application/x-www-form-urlencoded', 'token': alapi_token})
        res = json.loads(res.text)
        if res['code'] != 200:
            return False, res['msg']
        return True, res['data']['pinyin']
    except Exception as e:
        return False, repr(e)


def exchange(fr, number, to=user_currency):
    """
    查询<number> <fr> 对应 多少 <to>

    Query <number> <fr> corresponding <number?> <to>

    :param to: 待查询的币种
    :param number: 待查询的货币数量
    :param fr: 目标币种
    :return:
    """

    try:
        res = requests.get(v2_url + 'exchange',
                           params={'money': number, 'from': fr, 'to': to},
                           headers={'Content-Type': 'application/x-www-form-urlencoded', 'token': alapi_token})
        res = json.loads(res.text)
        if res['code'] != 200:
            return False, res['msg']
        return True, res['data']
    except Exception as e:
        return False, repr(e)


def zhihuDaily():
    """
    获取知乎日报

    Get Zhihu Daily

    :return:
    """
    try:
        res = requests.get(v2_url + 'zhihu',
                           headers={'Content-Type': 'application/x-www-form-urlencoded', 'token': alapi_token})
        res = json.loads(res.text)
        if res['code'] != 200:
            return False, res['msg']
        return True, res['data']
    except Exception as e:
        return False, repr(e)


def daily60s():
    """
    获取每日60秒早报

    Get the daily 60-second morning report

    :return:
    """
    try:
        res = requests.get(v2_url + 'zaobao?format=json', headers={'token': alapi_token})
        res = json.loads(res.text)

        if res['code'] != 200:
            return False, res['msg']
        return True, res['data']
    except Exception as e:
        return False, repr(e)
