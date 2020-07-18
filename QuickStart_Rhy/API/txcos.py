from QuickStart_Rhy import dir_char
from QuickStart_Rhy.API import pre_check
import qcloud_cos


class txcos:
    def __init__(self):
        """
        初始化并登陆腾讯云对象存储
        """
        scid = pre_check('txyun_scid')
        sckey = pre_check('txyun_sckey')
        self.region = pre_check('txyun_df_region')
        self.df_bucket = pre_check('txyun_cos_df_bucket')
        config = qcloud_cos.CosConfig(Region=self.region,
                                      SecretId=scid,
                                      SecretKey=sckey)
        self.client = qcloud_cos.CosS3Client(config)

    def get_func_table(self):
        """
        获取对象支持的函数表

        :return: 函数表
        """
        return {
            '-up': self.upload,
            '-rm': self.remove,
            '-dl': self.download,
            '-ls': self.list_bucket
        }

    def upload(self, filePath: str, bucket=None):
        """
        上传文件

        :param filePath: 文件地址
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        filename = filePath.split(dir_char)[-1]
        self.client.upload_file(Bucket=bucket, LocalFilePath=filePath, Key=filename)

    def download(self, filename: str, bucket=None):
        """
        下载文件

        :param filename: 文件在桶中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from QuickStart_Rhy.NetTools.normal_dl import normal_dl
        bucket = bucket if bucket else self.df_bucket
        url = 'https://' + bucket + '.cos.' + self.region + '.myqcloud.com/' + filename
        normal_dl(url)  # * 由于腾讯云没有提供可调用的下载sdk，因此使用qs下载引擎下载

    def remove(self, filePath: str, bucket=None):
        """
        删除桶中的文件

        :param filePath: 文件在桶中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        self.client.delete_object(bucket, filePath)

    def list_bucket(self, bucket=None):
        """
        展示桶中的全部文件信息

        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from QuickStart_Rhy.NetTools.normal_dl import size_format
        from prettytable import PrettyTable
        bucket = bucket if bucket else self.df_bucket
        ls = self.client.list_objects(Bucket=bucket)['Contents']
        tb = PrettyTable(['File', 'Size'])
        for obj in ls:
            tb.add_row([obj['Key'], size_format(int(obj['Size']), align=True)])
        print('Bucket Url: https://' + bucket + '.cos.' + self.region + '.myqcloud.com/')
        print(tb)
