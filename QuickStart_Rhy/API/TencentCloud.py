# coding=utf-8
"""
腾讯云相关API

Tencent cloud API
"""
import json
from .. import requirePackage
from . import pre_check, user_lang, dir_char


class TxCOS:
    qcloud_cos = requirePackage('qcloud_cos', real_name='cos-python-sdk-v5')

    def __init__(self):
        """
        初始化并登陆腾讯云对象存储

        Initialize and log in Tencent Cloud object storage
        """
        scid = pre_check('txyun_scid')
        sckey = pre_check('txyun_sckey')
        self.region = pre_check('txyun_df_region')
        self.df_bucket = pre_check('txyun_cos_df_bucket')
        self.cdn_url = pre_check('txyun_df_cdn_url', ext=False)
        if self.cdn_url and not self.cdn_url.endswith('/'):
            self.cdn_url += '/'
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

    def upload(self, filePath: str, bucket: str = None, key: str = None):
        """
        上传文件

        Upload file

        :param key: 在COS上的文件路径
        :param filePath: 文件地址
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        filename = filePath.strip()
        self.client.upload_file(Bucket=bucket, LocalFilePath=filename, Key=key if key else filename.replace(dir_char, '/'))

    def download(self, filename: str, bucket: str = None):
        """
        下载文件

        Download file

        :param filename: 文件在桶中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from ..NetTools.NormalDL import normal_dl
        bucket = bucket if bucket else self.df_bucket

        url = self.cdn_url + filename \
            if bucket == self.df_bucket and self.cdn_url else \
            'https://' + bucket + '.cos.' + self.region + '.myqcloud.com/' + filename
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
        from .. import qs_default_console, qs_info_string
        from ..NetTools.NormalDL import size_format
        from ..TuiTools.Table import qs_default_table
        from rich.text import Text
        bucket = bucket if bucket else self.df_bucket
        ls = self.client.list_objects(Bucket=bucket)['Contents']
        tb = qs_default_table(['File', 'Size'] if user_lang != 'zh' else ['文件', '体积'], title='Tencnet COS')
        for obj in ls:
            tb.add_row(Text(obj['Key'], justify='left'), Text(size_format(int(obj['Size']), align=True), justify='right'))
        qs_default_console.print(qs_info_string, 'Bucket Url:' if user_lang != 'zh' else '桶链接:',
                                 self.cdn_url if bucket == self.df_bucket and self.cdn_url else
                                 'https://' + bucket + '.cos.' + self.region + '.myqcloud.com/')
        qs_default_console.print(tb, justify="center")


class Translate:
    requirePackage('tencentcloud', real_name='tencentcloud-sdk-python')
    detect = requirePackage('langdetect', 'detect')
    DetectorFactory = requirePackage('langdetect', 'DetectorFactory')

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

    @staticmethod
    def langdetect(text: str) -> str:
        """
        获取文本的语言类型

        Gets the language type of the text

        :param text: 待识别文本
        :return: 语言类型
        """
        return Translate.detect(text)

    def translate(self, text: str, from_lang: str = None, to_lang: str = user_lang) -> str:
        """
        翻译文本至默认语言

        Translate text to the default language

        :param from_lang: 文本语言
        :param to_lang: 目标语言
        :param text: 文本
        :return: 翻译结果
        """
        req = Translate.models.TextTranslateRequest()
        req.from_json_string(json.dumps({
            "SourceText": text,
            "Source": self.langdetect(text) if not from_lang else from_lang,
            "Target": to_lang,
            "ProjectId": 0
        }))
        return json.loads(self.client.TextTranslate(req).to_json_string())['TargetText']


def translate(text: str, from_lang: str = None, to_lang: str = user_lang) -> str:
    return Translate().translate(text, from_lang, to_lang)
