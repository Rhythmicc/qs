from QuickStart_Rhy.API import *
import qiniu


class Qiniu_oss_api:
    def __init__(self):
        self.ac_key = pre_check('qiniu_ac_key')
        self.sc_key = pre_check('qiniu_sc_key')
        self.auth = qiniu.Auth(self.ac_key, self.sc_key)
        self.df_bucket = pre_check('qiniu_bk_name')

    def get_func_table(self):
        return {
            '-up': self.upload,
            '-rm': self.remove,
            '-cp': self.copy_url,
            '-dl': self.download,
            '-ls': self.list_bucket
        }

    def upload(self, filePath: str, bucket=None):
        tk = self.auth.upload_token(bucket if bucket else self.df_bucket, filePath.split(dir_char)[-1])
        qiniu.put_file(tk, filePath.split(dir_char)[-1], filePath)

    def remove(self, filePath: str, bucket=None):
        bk = qiniu.BucketManager(self.auth)
        bk.delete(bucket if bucket else self.df_bucket, filePath)

    def copy_url(self, filePath: str, bucket=None):
        bk = qiniu.BucketManager(self.auth)
        bk.fetch(filePath, bucket if bucket else self.df_bucket, filePath.split('/')[-1])

    def get_bucket_url(self, bucket=None):
        import requests
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
        from prettytable import PrettyTable
        bk = qiniu.BucketManager(self.auth)
        ret = bk.list(bucket if bucket else self.df_bucket)
        if not ret[1]:
            print("ERROR!")
            exit(0)
        root_url = 'http://' + self.get_bucket_url(bucket)[0] + '/'
        ret = ret[0]['items']
        from QuickStart_Rhy.NetTools.normal_dl import size_format
        tb = PrettyTable(['File', 'Size'])
        for i in ret:
            tb.add_row([i['key'], size_format(i['fsize'])])
        print("Bucket url:", root_url)
        print(tb)

    def download(self, filePath: str, bucket=None):
        from QuickStart_Rhy.NetTools.normal_dl import normal_dl
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
