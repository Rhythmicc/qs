from QuickStart_Rhy import dir_char
from QuickStart_Rhy.API import pre_check
import qcloud_cos


class txcos:
    def __init__(self):
        scid = pre_check('txyun_scid')
        sckey = pre_check('txyun_sckey')
        self.region = pre_check('txyun_df_region')
        self.df_bucket = pre_check('txyun_cos_df_bucket')
        config = qcloud_cos.CosConfig(Region=self.region,
                                      SecretId=scid,
                                      SecretKey=sckey)
        self.client = qcloud_cos.CosS3Client(config)

    def get_func_table(self):
        return {
            '-up': self.upload,
            '-rm': self.remove,
            '-dl': self.download,
            '-ls': self.list_bucket
        }

    def upload(self, filePath: str, bucket=None):
        bucket = bucket if bucket else self.df_bucket
        filename = filePath.split(dir_char)[-1]
        self.client.upload_file(Bucket=bucket, LocalFilePath=filePath, Key=filename)

    def download(self, filename: str, bucket=None):
        from QuickStart_Rhy.NetTools.normal_dl import normal_dl
        bucket = bucket if bucket else self.df_bucket
        url = 'https://' + bucket + '.cos.' + self.region + '.myqcloud.com/' + filename
        normal_dl(url)

    def remove(self, filePath: str, bucket=None):
        bucket = bucket if bucket else self.df_bucket
        self.client.delete_object(bucket, filePath)

    def list_bucket(self, bucket=None):
        from QuickStart_Rhy.NetTools.normal_dl import size_format
        from prettytable import PrettyTable
        bucket = bucket if bucket else self.df_bucket
        ls = self.client.list_objects(Bucket=bucket)['Contents']
        tb = PrettyTable(['File', 'Size'])
        for obj in ls:
            tb.add_row([obj['Key'], size_format(int(obj['Size']), align=True)])
        print('Bucket Url: https://' + bucket + '.cos.' + self.region + '.myqcloud.com/')
        print(tb)
