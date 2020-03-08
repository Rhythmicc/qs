from prettytable import PrettyTable
import requests
import json
import sys
import os

dir_char = '\\' if sys.platform.startswith('win') else '/'
user_root = os.path.expanduser('~')
if os.path.exists(user_root + dir_char + '.qsrc'):
    with open(user_root + dir_char + '.qsrc', 'r') as f:
        qsconfig = json.loads(f.read())
else:
    with open(user_root + dir_char + '.qsrc', 'w') as f:
        f.write('{\n'
                '  "rmbg": "GET API KEY: https://www.remove.bg"\n'
                '  "smms": "GET API KEY: https://sm.ms"\n'
                '}')
    qsconfig = {}


def pre_check(funcName: str) -> str:
    try:
        api_key = qsconfig[funcName]
        if not api_key:
            exit('You should set %s api key at: %s' % (funcName, user_root + dir_char + '.qsrc'))
    except KeyError:
        exit('You should set %s api key at: %s' % (funcName, user_root + dir_char + '.qsrc'))
    else:
        return api_key


def rmbg(filePath: str):
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
        exit('Usage: %s {*.md} | {picture}' % sys.argv[0])
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


class Aliyun_nas_api:
    def __init__(self):
        self.ac_id = pre_check('aliyun_nas_acid')
        self.ac_key = pre_check('aliyun_nas_ackey')
        self.bucket_url = pre_check('aliyun_nas_bucket_url')

    def upload(self, filePath: str, bucket=pre_check('aliyun_nas_df_bucket')):
        import oss2
        auth = oss2.Auth(self.ac_id, self.ac_key)
        bucket = oss2.Bucket(auth, self.bucket_url, bucket)
        oss2.resumable_upload(bucket, filePath.split(dir_char)[-1], filePath, num_threads=4)

    def download(self, filename: str, bucket=pre_check('aliyun_nas_df_bucket')):
        import oss2
        auth = oss2.Auth(self.ac_id, self.ac_key)
        bucket = oss2.Bucket(auth, self.bucket_url, bucket)
        oss2.resumable_download(bucket, filename, filename, num_threads=4)


class Qiniu_nas_api:
    def __init__(self):
        self.ac_key = pre_check('qiniu_ac_key')
        self.sc_key = pre_check('qiniu_sc_key')

    def upload(self, filePath: str, bucket=pre_check('qiniu_bk_name')):
        import qiniu
        auth = qiniu.Auth(self.ac_key, self.sc_key)
        tk = auth.upload_token(bucket, filePath.split(dir_char)[-1])
        qiniu.put_file(tk, filePath.split(dir_char)[-1], filePath)

    def remove(self, filePath: str, bucket=pre_check('qiniu_bk_name')):
        import qiniu
        auth = qiniu.Auth(self.ac_key, self.sc_key)
        bk = qiniu.BucketManager(auth)
        bk.delete(bucket, filePath)

    def copy_url(self, filePath: str, bucket=pre_check('qiniu_bk_name')):
        import qiniu
        auth = qiniu.Auth(self.ac_key, self.sc_key)
        bk = qiniu.BucketManager(auth)
        bk.fetch(filePath, bucket, filePath.split('/')[-1])
