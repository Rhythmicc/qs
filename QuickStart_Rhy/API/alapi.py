# coding=utf-8
from QuickStart_Rhy.API import *
from urllib.parse import quote
import requests

alapi_token = pre_check('alapi_token', False)


def upload_image(filePath: str, plt_type: str = 'Ali'):
    """
    上传图片或Markdown中所有的图片到多平台（免API KEY，但不保证数据安全）

    Upload images or all images from Markdown to multiple platforms (API-free KEY, but data security is not guaranteed)

    :param filePath: 图片或Markdown文件路径
    :param plt_type: 平台（使用 qs -upload_image -help查看支持的平台）
    :return: None
    """
    from prettytable import PrettyTable

    def post_img(path):
        if not os.path.exists(path):
            return False
        try:
            data = {'type': plt_type}
            file = [('image', open(path, 'rb'))]
        except:
            return False
        res_json = requests.post('https://v1.alapi.cn/api/image', data=data, files=file).text \
            if not alapi_token else \
            requests.post('https://v1.alapi.cn/api/image', data=data, files=file, headers={'token': alapi_token}).text
        return json.loads(res_json)

    def get_path(rt, rel):
        return os.path.abspath(rt + rel)

    def format_markdown(path):
        import re
        _user_path = os.path.expanduser('~')
        rt_path = dir_char.join(os.path.abspath(path).split(dir_char)[:-1]) + dir_char
        res_tb = PrettyTable()
        res_tb.field_names = ['File', 'Status', 'url'] if user_lang != 'zh' else ['文件', '状态', '链接']
        img_set = {}
        with open(path, 'r') as fp:
            ct = fp.read()
        aims = re.findall('!\[.*?]\((.*?)\)', ct, re.M)
        for aim in aims:
            raw_path = aim
            aim = aim.replace('~', _user_path)
            aim = aim if aim.startswith(dir_char) else get_path(rt_path, aim)
            if aim not in img_set:
                res_dict = post_img(aim)
                if not res_dict:
                    res_tb.add_row([aim.split(dir_char)[-1], 'No File', ''])
                    img_set[aim] = False
                else:
                    res_plt = list(res_dict['data']['url'].keys())[0]
                    res_tb.add_row([aim.split(dir_char)[-1], res_dict['msg'],
                                    '' if res['code'] != 200 else (
                                        res_dict['data']['url'][res_plt]
                                        if res_dict['data']['url'][res_plt].lower() != 'null'
                                        else res_plt + ' failed')]
                                   )
                    if res_dict['code'] != 200:
                        break
                    img_set[aim] = res_dict['data']['url'][res_plt] if res_dict['code'] != 200 else False
            if img_set[aim]:
                ct = ct.replace(raw_path, img_set[aim])
        with open(path, 'w') as fp:
            fp.write(ct)
        print(res_tb)

    try:
        is_md = filePath.endswith('.md')
    except IndexError:
        exit('Usage: qs -upimg {*.md} | {picture}' if user_lang != 'zh' else '使用: qs -upimg {Markdown文件} 或 {任意图片文件}')
    else:
        if is_md:
            format_markdown(filePath)
        else:
            res = post_img(filePath)
            tb = PrettyTable(['File', 'Status', 'url'])
            if not res:
                tb.add_row([filePath.split(dir_char)[-1], 'No File', ''])
            else:
                plt_type = list(res['data']['url'].keys())[0]
                tb.add_row([filePath.split(dir_char)[-1], res['msg'],
                            '' if res['code'] != 200 else (res['data']['url'][plt_type]
                            if res['data']['url'][plt_type] else plt_type + ' failed')])
            print(tb)


def translate(text: str, from_lang: str = None, to_lang: str = user_lang):
    """
    获取翻译结果

    Get the translation results.
    
    :param text: 待翻译内容 | Content to be translated.
    :param from_lang: 语种来源 | Source language
    :param to_lang: 翻译成的语种 | Translated into the language
    :return: 翻译的文本 | Translated text
    """
    request_info = 'q={}&from={}&to={}'.format(quote(text, 'utf-8'), from_lang, to_lang) if from_lang \
        else 'q={}&to={}'.format(quote(text, 'utf-8'), to_lang)
    res = requests.post('https://v1.alapi.cn/api/fanyi', data=request_info,
                        headers={'Content-Type': "application/x-www-form-urlencoded", 'token': alapi_token}
                        if alapi_token else {'Content-Type': 'application/x-www-form-urlencoded'})
    if res.status_code == requests.codes.ok:
        res = json.loads(res.text)
        if res['code'] != 200:
            return "[ERROR] {}".format(res['msg'])
        return res['data']['trans_result'][0]['dst']
    return "[ERROR] 未知错误 | Unknown Error"


def bili_cover(url: str):
    """
    获取BiliBili视频封面

    Get the BiliBili video cover

    :param url: BiliBili视频链接或视频号 | BiliBili video link or video number
    :return:
    """
    import re
    from QuickStart_Rhy.NetTools.NormalDL import normal_dl
    res = requests.post('https://v1.alapi.cn/api/bbcover', data='c='+url,
                        headers={'Content-Type': 'application/x-www-form-urlencoded', 'token': alapi_token}
                        if alapi_token else {'Content-Type': 'application/x-www-form-urlencoded'})
    if res.status_code == requests.codes.ok:
        res = json.loads(res.text)
        if res['code'] != 200 or res['msg'] != 'success':
            print(("[ERROR] Get cover with: %s failed" if user_lang != 'zh' else '[错误] 下载封面: %s 失败') % url)
            return
        res = res['data']
        res['description'] = res['description'].replace('<br />', '\n\t')
        res['description'] = res['description'].replace('&nbsp;', ' ')
        res['description'] = re.sub('<.*?>', '', res['description']).strip()  # 忽略HTML标签
        print('[TITLE]' if user_lang != 'zh' else '[标题]', '%s' % res['title'])
        print('[INFO ]' if user_lang != 'zh' else '[简介]', end='\n\t')
        print(res['description'], end='\n\n')
        normal_dl(res['cover'], res['title'] + '.' + res['cover'].split('.')[-1])
    else:
        print(("[ERROR] Get cover with: %s failed" if user_lang != 'zh' else '[错误] 下载封面: %s 失败') % url)


def ip_info(ip: str):
    """
    获取ip的运营商、地理位置等数据

    Get IP operator, geographic location and other data

    :param ip: ipv4, ipv6, empty means current machine
    :return: data dict
    """
    res = requests.post('https://v1.alapi.cn/api/ip', data="ip=%s&format=json" % ip,
                        headers={'Content-Type': "application/x-www-form-urlencoded", 'token': alapi_token}
                        if ip and alapi_token else {'Content-Type': 'application/x-www-form-urlencoded'}
                        if ip else headers.update({'token': alapi_token} if alapi_token else headers))
    try:
        res = json.loads(res.text)
        if res['code'] != 200:
            return [ip, '', res['msg'], '{code, %s}' % res['code']]
        return res['data']
    except :
        print(res.text)
        return [ip, '', '网络错误', '{code, %s}' % res.status_code]


def garbage_classification(query_ls: list):
    """
    查询中国垃圾分类

    Search Chinese garbage classification

    :param query_ls: 待查询的垃圾列表 | garbage list
    :return: 查询结果的字符串表格 | string table
    """
    def fmt_string(string, pre_num):
        return '\n' * pre_num + '\n'.join([string[i: i+10] for i in range(0, len(string), 10)])

    import prettytable
    import math
    table = prettytable.PrettyTable(['名称', '分类', '解释', '提示'])
    first_flag = True
    for query_el in query_ls:
        if first_flag:
            first_flag = False
        else:
            table.add_row(['-'] * 4)
        res = requests.post("https://v1.alapi.cn/api/lajifenlei", data="name={}".format(quote(query_el, 'utf-8')),
                            headers={'Content-Type': "application/x-www-form-urlencoded", 'token': alapi_token}
                            if alapi_token else {'Content-Type': 'application/x-www-form-urlencoded'})
        if res.status_code == requests.codes.ok:
            res = json.loads(res.text)
            if res['code'] != 200:
                table.add_row([fmt_string(query_el, 0), '', '', fmt_string(res['msg'], 0)])
                continue
            try:
                res = res['data'][0]
                half_rows = [math.ceil(len(query_el) / 20), 1, math.ceil(len(res['explain']) / 20),
                             math.ceil(len(res['tip']) / 20)]
                max_row = max(half_rows)
                half_rows = [max_row - i for i in half_rows]
                table.add_row([fmt_string(query_el, half_rows[0]),
                               fmt_string(['可回收', '有害', '厨余(湿)', '其他(干)'][res['type']-1], half_rows[1]),
                               fmt_string(res['explain'], half_rows[2]), fmt_string(res['tip'], half_rows[3])])
            except IndexError:
                table.add_row([fmt_string(query_el, 0), 'Unknown', '未知垃圾', '未知垃圾'])
        else:
            table.add_row([fmt_string(query_el, 0), 'Unknown', 'None', 'Request Error'])
    return str(table)


def short_video_info(url: str):
    """
    解析多平台短视频，并返回视频信息与下载直链

    Parse multi - platform short video and return video information with download straight link

    :param url: 短视频分享链接 | Short video sharing link
    :return:
    """
    res = requests.post("https://v1.alapi.cn/api/video/url", data="url={}".format(quote(url, 'utf-8')),
                        headers={'Content-Type': "application/x-www-form-urlencoded", 'token': alapi_token}
                        if alapi_token else {'Content-Type': "application/x-www-form-urlencoded"})
    try:
        res = json.loads(res.text)
        if res['code'] != 200:
            return False, {'title': res['msg'], 'cover_url': 'None', 'video_url': 'None', 'source': res['code']}
        return True, res['data']
    except :
        return False, {'title': '网络错误' if user_lang == 'zh' else 'Network Error',
                       'cover_url': 'None', 'video_url': 'None', 'source': 'Unknown'}


def acg():
    """
    随机获取一张acg图片链接

    Get a random link to an ACG image

    :return: acg image link
    """
    res = requests.post('https://v1.alapi.cn/api/acg', data='format=json',
                        headers={'Content-Type': "application/x-www-form-urlencoded", 'token': alapi_token}
                        if alapi_token else {'Content-Type': "application/x-www-form-urlencoded"})
    try:
        res = json.loads(res.text)
        if res['code'] != 200:
            return False, res['msg'], 0, 0
        return True, res['data']['url'], res['data']['width'], res['data']['height']
    except :
        return False, ('Network Error' if user_lang != 'zh' else '网络错误'), 0, 0
