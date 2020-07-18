from QuickStart_Rhy.API import *
import oss2


class Aliyun_oss_api:
    def __init__(self, ac_id=pre_check('aliyun_oss_acid'), ac_key=pre_check('aliyun_oss_ackey'),
                 bucket_url=pre_check('aliyun_oss_bucket_url'), df_bucket=pre_check('aliyun_oss_df_bucket')):
        """
        初始化并登陆阿里云对象存储

        :param ac_id: Access id
        :param ac_key: Access key
        :param bucket_url: oss-地区.aliyuncs.com
        :param df_bucket: 桶名称
        """
        self.ac_id = ac_id
        self.ac_key = ac_key
        self.bucket_url = bucket_url
        self.df_bucket = df_bucket
        self.auth = oss2.Auth(self.ac_id, self.ac_key)

    def get_func_table(self):
        """
        获取OSS类支持的操作
        :return: 支持的函数字典
        """
        return {
            '-up': self.upload,
            '-rm': self.remove,
            '-dl': self.download,
            '-ls': self.list_bucket
        }

    def upload(self, filePath: str, bucket=None):
        """
        上传文件（支持断点续传）

        :param filePath: 文件路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        oss2.resumable_upload(bucket, filePath.split(dir_char)[-1], filePath, num_threads=4)

    def download(self, filename: str, bucket=None):
        """
        下载文件（支持断点续传）

        :param filename: 文件在bucket中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        oss2.resumable_download(bucket, filename, filename, num_threads=4)

    def remove(self, filePath: str, bucket=None):
        """
        删除文件

        :param filePath: 文件在bucket中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        bucket.delete_object(filePath)

    def list_bucket(self, bucket=None):
        """
        打印桶中的文件表

        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from QuickStart_Rhy.NetTools.normal_dl import size_format
        from prettytable import PrettyTable
        bucket = bucket if bucket else self.df_bucket
        ls = oss2.Bucket(self.auth, self.bucket_url, bucket)
        tb = PrettyTable(['File', 'Size'])
        for obj in oss2.ObjectIterator(ls):
            tb.add_row([obj.key, size_format(obj.size)])
        print('Bucket Url:', 'https://' + bucket + '.' + self.bucket_url + '/')
        print(tb)
