# coding=utf-8
"""
腾讯云相关API

Tencent cloud API
"""
import json
from .. import requirePackage, user_lang
from . import pre_check


class TxCOS:
    def __init__(self, scid=None, sckey=None, region=None, bucket=None, cdn_url=None):
        """
        初始化并登陆腾讯云对象存储

        Initialize and log in Tencent Cloud object storage

        :param scid: SecretId
        :param sckey: SecretKey
        :param region: 地区
        :param bucket: 桶名称
        :param cdn_url: CDN地址

        :return: None
        """
        if not (scid and sckey and region and bucket):
            scid, sckey, self.region, self.df_bucket = pre_check(
                "txyun_scid", "txyun_sckey", "txyun_df_region", "txyun_cos_df_bucket"
            )
        self.cdn_url = (
            pre_check("txyun_df_cdn_url", ext=False) if not cdn_url else cdn_url
        )
        if self.cdn_url and not self.cdn_url.endswith("/"):
            self.cdn_url += "/"

        qcloud_cos = requirePackage("qcloud_cos", real_name="cos-python-sdk-v5")

        config = qcloud_cos.CosConfig(
            Region=self.region, SecretId=scid, SecretKey=sckey
        )
        self.client = qcloud_cos.CosS3Client(config)

    def get_func_table(self):
        """
        获取对象支持的函数表

        Gets a table of functions supported by the object

        :return: 函数表
        """
        return {
            "-up": self.upload,
            "-rm": self.remove,
            "-dl": self.download,
            "-ls": self.list_bucket,
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
        from .. import dir_char

        bucket = bucket if bucket else self.df_bucket
        filename = filePath.strip()
        self.client.upload_file(
            Bucket=bucket,
            LocalFilePath=filename,
            Key=key if key else filename.replace(dir_char, "/"),
        )

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

        url = (
            self.cdn_url + filename
            if bucket == self.df_bucket and self.cdn_url
            else "https://"
            + bucket
            + ".cos."
            + self.region
            + ".myqcloud.com/"
            + filename
        )
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
        ls = self.client.list_objects(Bucket=bucket)["Contents"]
        tb = qs_default_table(
            ["File", "Size"] if user_lang != "zh" else ["文件", "体积"], title="Tencnet COS"
        )
        for obj in ls:
            tb.add_row(
                Text(obj["Key"], justify="left"),
                Text(size_format(int(obj["Size"]), align=True), justify="right"),
            )
        qs_default_console.print(
            qs_info_string,
            "Bucket Url:" if user_lang != "zh" else "桶链接:",
            self.cdn_url
            if bucket == self.df_bucket and self.cdn_url
            else "https://" + bucket + ".cos." + self.region + ".myqcloud.com/",
        )
        qs_default_console.print(tb, justify="center")


class Translate:

    from tencentcloud.tmt.v20180321 import models

    def __init__(self, scid, sckey, region):
        """
        初始化并登陆腾讯翻译接口

        Initialize and log in Tencent translation interface

        :param scid: secret id
        :param sckey: secret key
        :param region: 地区
        """
        if not (scid and sckey and region):
            scid, sckey, region = pre_check(
                "txyun_scid", "txyun_sckey", "txyun_df_region"
            )
        requirePackage("langdetect", "DetectorFactory").seed = 0
        cred = requirePackage(
            "tencentcloud.common", "credential", real_name="tencentcloud-sdk-python"
        )
        http_profile = requirePackage(
            "tencentcloud.common.profile.http_profile",
            "HttpProfile",
            real_name="tencentcloud-sdk-python",
        )()
        http_profile.endpoint = "tmt.tencentcloudapi.com"
        clientProfile = requirePackage(
            "tencentcloud.common.profile.client_profile",
            "ClientProfile",
            real_name="tencentcloud-sdk-python",
        )()
        clientProfile.httpProfile = http_profile
        self.client = requirePackage(
            "tencentcloud.tmt.v20180321.tmt_client",
            "TmtClient",
            real_name="tencentcloud-sdk-python",
        )(cred, region, clientProfile)

    @staticmethod
    def langdetect(text: str) -> str:
        """
        获取文本的语言类型

        Gets the language type of the text

        :param text: 待识别文本
        :return: 语言类型
        """
        return requirePackage("langid", "classify")(text)[0]

    def translate(
        self, text: str, from_lang: str = None, target_lang: str = user_lang
    ) -> str:
        """
        翻译文本至默认语言

        Translate text to the default language

        :param from_lang: 文本语言
        :param target_lang: 目标语言
        :param text: 文本
        :return: 翻译结果
        """
        req = requirePackage(
            "tencentcloud.tmt.v20180321.models", "TextTranslateRequest"
        )()
        req.from_json_string(
            json.dumps(
                {
                    "SourceText": text,
                    "Source": self.langdetect(text) if not from_lang else from_lang,
                    "Target": target_lang,
                    "ProjectId": 0,
                }
            )
        )
        return json.loads(self.client.TextTranslate(req).to_json_string())["TargetText"]


def translate(text: str, from_lang: str = None, target_lang: str = user_lang) -> str:
    return Translate().translate(text, from_lang, target_lang)
