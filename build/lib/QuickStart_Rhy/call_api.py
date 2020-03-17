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


class Aliyun_oss_api:
    def __init__(self):
        import oss2
        self.ac_id = pre_check('aliyun_oss_acid')
        self.ac_key = pre_check('aliyun_oss_ackey')
        self.bucket_url = pre_check('aliyun_oss_bucket_url')
        self.df_bucket = pre_check('aliyun_oss_df_bucket')
        self.auth = oss2.Auth(self.ac_id, self.ac_key)

    def upload(self, filePath: str, bucket=None):
        import oss2
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        oss2.resumable_upload(bucket, filePath.split(dir_char)[-1], filePath, num_threads=4)

    def download(self, filename: str, bucket=None):
        import oss2
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        oss2.resumable_download(bucket, filename, filename, num_threads=4)

    def remove(self, filePath: str, bucket=None):
        import oss2
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        bucket.delete_object(filePath)

    def list_bucket(self, bucket=None):
        from QuickStart_Rhy.normal_dl import size_format
        import oss2
        bucket = bucket if bucket else self.df_bucket
        ls = oss2.Bucket(self.auth, self.bucket_url, bucket)
        tb = PrettyTable(['File', 'Size'])
        for obj in oss2.ObjectIterator(ls):
            tb.add_row([obj.key, size_format(obj.size)])
        print('Bucket Url:', 'https://'+bucket+'.'+self.bucket_url+'/')
        print(tb)


class Qiniu_oss_api:
    def __init__(self):
        import qiniu
        self.ac_key = pre_check('qiniu_ac_key')
        self.sc_key = pre_check('qiniu_sc_key')
        self.auth = qiniu.Auth(self.ac_key, self.sc_key)
        self.df_bucket = pre_check('qiniu_bk_name')

    def upload(self, filePath: str, bucket=None):
        import qiniu
        tk = self.auth.upload_token(bucket if bucket else self.df_bucket, filePath.split(dir_char)[-1])
        qiniu.put_file(tk, filePath.split(dir_char)[-1], filePath)

    def remove(self, filePath: str, bucket=None):
        import qiniu
        bk = qiniu.BucketManager(self.auth)
        bk.delete(bucket if bucket else self.df_bucket, filePath)

    def copy_url(self, filePath: str, bucket=None):
        import qiniu
        bk = qiniu.BucketManager(self.auth)
        bk.fetch(filePath, bucket if bucket else self.df_bucket, filePath.split('/')[-1])

    def get_bucket_url(self, bucket=None):
        bucket = bucket if bucket else self.df_bucket
        url = 'http://api.qiniu.com/v6/domain/list?tbl=%s' % bucket
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "QBox %s" % self.auth.token_of_request(url)
        }
        res = requests.get(url, headers=headers)
        if res.status_code == requests.codes.ok:
            return res.json()
        else:
            return False

    def list_bucket(self, bucket=None):
        import qiniu
        bk = qiniu.BucketManager(self.auth)
        ret = bk.list(bucket if bucket else self.df_bucket)
        if not ret[1]:
            print("ERROR!")
            exit(0)
        root_url = 'http://' + self.get_bucket_url(bucket)[0] + '/'
        ret = ret[0]['items']
        from QuickStart_Rhy.normal_dl import size_format
        tb = PrettyTable(['File', 'Size'])
        for i in ret:
            tb.add_row([i['key'], size_format(i['fsize'])])
        print("Bucket url:", root_url)
        print(tb)

    def download(self, filePath: str, bucket=None):
        from QuickStart_Rhy.normal_dl import normal_dl
        bucket = bucket if bucket else self.df_bucket
        root_url = self.get_bucket_url(bucket)[0]
        if root_url:
            root_url = 'http://' + root_url + '/'
        else:
            exit('Get Bucket Url Failed!')
        dl_url = root_url + filePath
        if bucket.startswith('admin'):
            dl_url = self.auth.private_download_url(dl_url)
        normal_dl(dl_url)
