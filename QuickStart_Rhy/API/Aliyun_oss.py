from QuickStart_Rhy.API import *
import oss2


class Aliyun_oss_api:
    def __init__(self):
        self.ac_id = pre_check('aliyun_oss_acid')
        self.ac_key = pre_check('aliyun_oss_ackey')
        self.bucket_url = pre_check('aliyun_oss_bucket_url')
        self.df_bucket = pre_check('aliyun_oss_df_bucket')
        self.auth = oss2.Auth(self.ac_id, self.ac_key)

    def get_func_table(self):
        return {
            '-up': self.upload,
            '-rm': self.remove,
            '-dl': self.download,
            '-ls': self.list_bucket
        }

    def upload(self, filePath: str, bucket=None):
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        oss2.resumable_upload(bucket, filePath.split(dir_char)[-1], filePath, num_threads=4)

    def download(self, filename: str, bucket=None):
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        oss2.resumable_download(bucket, filename, filename, num_threads=4)

    def remove(self, filePath: str, bucket=None):
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        bucket.delete_object(filePath)

    def list_bucket(self, bucket=None):
        from QuickStart_Rhy.NetTools.normal_dl import size_format
        from prettytable import PrettyTable
        bucket = bucket if bucket else self.df_bucket
        ls = oss2.Bucket(self.auth, self.bucket_url, bucket)
        tb = PrettyTable(['File', 'Size'])
        for obj in oss2.ObjectIterator(ls):
            tb.add_row([obj.key, size_format(obj.size)])
        print('Bucket Url:', 'https://'+bucket+'.'+self.bucket_url+'/')
        print(tb)
