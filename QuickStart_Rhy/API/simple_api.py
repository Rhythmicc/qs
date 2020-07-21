from QuickStart_Rhy.API import *
import requests


def rmbg(filePath: str):
    """
    删除图片背景

    :param filePath: 图片的路径
    :return: None
    """
    api_key = pre_check('rmbg')
    res = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(filePath, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': api_key},
    )
    if res.status_code == requests.codes.ok:
        img_name = filePath.split(dir_char)[-1].split('.')[0]
        if dir_char in filePath:
            img_root = dir_char.join(filePath.split(dir_char)[:-1]) + dir_char
        else:
            img_root = ''
        with open(img_root + img_name + '_rmbg.png', 'wb') as imgfile:
            imgfile.write(res.content)
    else:
        print('ERROR:', res.status_code, res.text)


def smms(filePath: str):
    """
    上传图片或Markdown中所有的图片到smms中

    :param filePath: 图片或Markdown文件的路径
    :return: None
    """
    from prettytable import PrettyTable
    api_key = pre_check('smms')

    def post_img(path):
        headers = {
            'Authorization': api_key,
        }
        try:
            data = {
                'smfile': (path.split('/')[-1], open(path, 'rb')),
                'format': 'json'
            }
        except:
            return False
        res_json = requests.post('https://sm.ms/api/v2/upload', headers=headers, files=data).text
        return json.loads(res_json)

    def get_path(rt, rel):
        return os.path.abspath(rt + rel)

    def format_markdown(path):
        import re
        _user_path = os.path.expanduser('~')
        rt_path = dir_char.join(os.path.abspath(path).split(dir_char)[:-1]) + dir_char
        res_tb = PrettyTable()
        res_tb.field_names = ['File', 'Status', 'url']
        img_set = {}
        with open(path, 'r') as fp:
            ct = fp.read()
        aims = re.findall('!\[.*?\]\((.*?)\)', ct, re.M)
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
                    res_tb.add_row(
                        [aim.split(dir_char)[-1], res_dict['success'],
                         res_dict['message'] if not res_dict['success'] else res_dict['data']['url']]
                    )
                    if not res_dict['success'] and res_dict['code'] == 'unauthorized':
                        break
                    img_set[aim] = res_dict['data']['url'] if res_dict['success'] else False
            if img_set[aim]:
                ct = ct.replace(raw_path, img_set[aim])
        with open(path, 'w') as fp:
            fp.write(ct)
        print(res_tb)

    try:
        is_md = filePath.endswith('.md')
    except IndexError:
        exit('Usage: qs {*.md} | {picture}')
    else:
        if is_md:
            format_markdown(filePath)
        else:
            res = post_img(filePath)
            tb = PrettyTable(['File', 'Status', 'url'])
            if not res:
                tb.add_row([filePath.split(dir_char)[-1], 'No File', ''])
            else:
                tb.add_row(
                    [filePath.split(dir_char)[-1], res['success'], '' if not res['success'] else res['data']['url']])
            print(tb)


def pasteme(key: str = '100', password: str = '', mode: str = 'get'):
    """
    利用pasteme实现的信息收发

    :param key: 信息编号
    :param password: 获取信息可能需要的密码
    :param mode: 'get' 或 'post'，get时将信息写入key.*文件中，post将剪切板内容上传至pasteme
    :return: None
    """
    import pyperclip
    from colorama import Fore, Style
    if mode == 'get':
        if password:
            r = requests.get('https://api.pasteme.cn/%s,%s' % (key, password), params={'json': True})
        else:
            r = requests.get('https://api.pasteme.cn/%s' % key, params={'json': True})
        if r.status_code == requests.codes.ok:
            js = json.loads(r.content)
            if js['status'] == 200:
                try:
                    pyperclip.copy(js['content'])
                except:
                    print("Sorry, but your system is not supported by `pyperclip`")
                with open("%s.%s" % (key, js['lang']), 'w') as file:
                    file.write(js['content'])
            else:
                print(Fore.RED, 'Wrong Password' if password else 'Password is required', Style.RESET_ALL)
        else:
            print(Fore.RED, 'Unknown error', Style.RESET_ALL)
    else:
        try:
            ss = pyperclip.paste()
        except :
            path = input('Sorry, but your system is not supported by `pyperclip`\nSo you need input file path: ')
            with open(path, 'r') as file:
                ss = file.read()
        js = {
            'lang': key if key else 'txt',
            'content': ss
        }
        if password:
            js['password'] = password
        r = requests.post('https://api.pasteme.cn',
                          headers={'Content-Type': 'application/json'},
                          json=js)
        if r.status_code == 201:
            print(json.loads(r.content))
        else:
            print('post failed')


def upimg(filePath: str, plt_type: str = 'Ali'):
    """
    上传图片或Markdown中所有的图片到多平台（免API KEY，但不保证数据安全）

    :param filePath: 图片或Markdown文件路径
    :param plt_type: 平台（使用 qs -upimg -help查看支持的平台）
    :return: None
    """
    from prettytable import PrettyTable

    def post_img(path):
        try:
            data = {'type': plt_type}
            file = [('image', open(path, 'rb'))]
        except:
            return False
        res_json = requests.post('https://v1.alapi.cn/api/image',
                                 data=data, files=file).text
        return json.loads(res_json)

    def get_path(rt, rel):
        return os.path.abspath(rt + rel)

    def format_markdown(path):
        import re
        _user_path = os.path.expanduser('~')
        rt_path = dir_char.join(os.path.abspath(path).split(dir_char)[:-1]) + dir_char
        res_tb = PrettyTable()
        res_tb.field_names = ['File', 'Status', 'url']
        img_set = {}
        with open(path, 'r') as fp:
            ct = fp.read()
        aims = re.findall('!\[.*?\]\((.*?)\)', ct, re.M)
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
                    res_tb.add_row([aim.split(dir_char)[-1], res_dict['msg'],
                                    '' if res['code'] != 200 else (
                                        res_dict['data']['url'][plt_type]
                                        if res_dict['data']['url'][plt_type].lower() != 'null'
                                        else plt_type + ' failed')]
                                   )
                    if res_dict['code'] != 200:
                        break
                    img_set[aim] = res_dict['data']['url'][plt_type] if res_dict['code'] != 200 else False
            if img_set[aim]:
                ct = ct.replace(raw_path, img_set[aim])
        with open(path, 'w') as fp:
            fp.write(ct)
        print(res_tb)

    try:
        is_md = filePath.endswith('.md')
    except IndexError:
        exit('Usage: qs {*.md} | {picture}')
    else:
        if is_md:
            format_markdown(filePath)
        else:
            res = post_img(filePath)
            tb = PrettyTable(['File', 'Status', 'url'])
            if not res:
                tb.add_row([filePath.split(dir_char)[-1], 'No File', ''])
            else:
                tb.add_row([filePath.split(dir_char)[-1], res['msg'],
                            '' if res['code'] != 200 else (
                                res['data']['url'][plt_type]
                                if res['data']['url'][plt_type].lower() != 'null' else plt_type + ' failed')]
                           )
            print(tb)
