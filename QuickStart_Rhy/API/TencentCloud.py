# coding=utf-8
from QuickStart_Rhy.API import *


class TxCOS:
    import qcloud_cos

    def __init__(self):
        """
        初始化并登陆腾讯云对象存储

        Initialize and log in Tencent Cloud object storage
        """
        scid = pre_check('txyun_scid')
        sckey = pre_check('txyun_sckey')
        self.region = pre_check('txyun_df_region')
        self.df_bucket = pre_check('txyun_cos_df_bucket')
        config = TxCOS.qcloud_cos.CosConfig(Region=self.region,
                                            SecretId=scid,
                                            SecretKey=sckey)
        self.client = TxCOS.qcloud_cos.CosS3Client(config)

    def get_func_table(self):
        """
        获取对象支持的函数表

        Gets a table of functions supported by the object

        :return: 函数表
        """
        return {
            '-up': self.upload,
            '-rm': self.remove,
            '-dl': self.download,
            '-ls': self.list_bucket
        }

    def upload(self, filePath: str, bucket: str = None):
        """
        上传文件

        Upload file

        :param filePath: 文件地址
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        filename = filePath.split(dir_char)[-1]
        self.client.upload_file(Bucket=bucket, LocalFilePath=filePath, Key=filename)

    def download(self, filename: str, bucket: str = None):
        """
        下载文件

        Download file

        :param filename: 文件在桶中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from QuickStart_Rhy.NetTools.NormalDL import normal_dl
        bucket = bucket if bucket else self.df_bucket
        url = 'https://' + bucket + '.cos.' + self.region + '.myqcloud.com/' + filename
        normal_dl(url)  # * 由于腾讯云没有提供可调用的下载sdk，因此使用qs下载引擎下载

    def remove(self, filePath: str, bucket: str = None):
        """
        删除桶中的文件

        Delete files in the bucket

        :param filePath: 文件在桶中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        self.client.delete_object(bucket, filePath)

    def list_bucket(self, bucket: str = None):
        """
        展示桶中的全部文件信息

        Displays all file information in the bucket

        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from QuickStart_Rhy.NetTools.NormalDL import size_format
        from prettytable import PrettyTable
        bucket = bucket if bucket else self.df_bucket
        ls = self.client.list_objects(Bucket=bucket)['Contents']
        tb = PrettyTable(['File', 'Size'] if user_lang != 'zh' else ['文件', '体积'])
        for obj in ls:
            tb.add_row([obj['Key'], size_format(int(obj['Size']), align=True)])
        print('Bucket Url:' if user_lang != 'zh' else '桶链接:',
              'https://' + bucket + '.cos.' + self.region + '.myqcloud.com/')
        print(tb)


class Translate:
    from langdetect import detect, DetectorFactory
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.tmt.v20180321 import tmt_client, models

    def __init__(self, scid: str = pre_check('txyun_scid'), sckey: str = pre_check('txyun_sckey'),
                 region: str = pre_check('txyun_df_region')):
        """
        初始化并登陆腾讯翻译接口

        Initialize and log in Tencent translation interface

        :param scid: secret id
        :param sckey: secret key
        :param region: 地区
        """
        Translate.DetectorFactory.seed = 0
        cred = Translate.credential.Credential(scid, sckey)
        http_profile = Translate.HttpProfile()
        http_profile.endpoint = "tmt.tencentcloudapi.com"
        clientProfile = Translate.ClientProfile()
        clientProfile.httpProfile = http_profile
        self.client = Translate.tmt_client.TmtClient(cred, region, clientProfile)

    def langdetect(self, text: str) -> str:
        """
        获取文本的语言类型

        Gets the language type of the text

        :param text: 待识别文本
        :return: 语言类型
        """
        return Translate.detect(text)

    def translate(self, text: str) -> dict:
        """
        翻译文本至默认语言

        Translate text to the default language

        :param text: 文本
        :return: 翻译结果
        """
        req = Translate.models.TextTranslateRequest()
        req.from_json_string(json.dumps({
            "SourceText": text,
            "Source": self.langdetect(text),
            "Target": user_lang,
            "ProjectId": 0
        }))
        return json.loads(self.client.TextTranslate(req).to_json_string())['TargetText']
