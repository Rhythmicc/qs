# coding=utf-8
"""
七牛云对象存储API

Qiniu cloud OSS API
"""
from . import pre_check, user_lang
from .. import requirePackage


class QiniuOSS:
    qiniu = requirePackage("qiniu")

    def __init__(
        self,
        ac_key: str = None,
        sc_key: str = None,
        df_bucket: str = None,
    ):
        """
        初始化并登陆七牛云对象存储

        Initializes and logs in qiniu cloud object storage

        :param ac_key: Access Key
        :param sc_key: Secret Key
        :param df_bucket: 默认桶名称
        """
        if not (ac_key and sc_key and df_bucket):
            ac_key, sc_key, df_bucket = pre_check(
                "qiniu_ac_key", "qiniu_sc_key", "qiniu_bk_name"
            )
        self.ac_key = ac_key
        self.sc_key = sc_key
        self.auth = QiniuOSS.qiniu.Auth(self.ac_key, self.sc_key)
        self.df_bucket = df_bucket
        self.bar, self.tid = None, None

    def get_func_table(self):
        """
        获取对象支持的操作

        Gets the operations supported by the object

        :return: 函数表
        """
        return {
            "-up": self.upload,
            "-rm": self.remove,
            "-cp": self.copy_url,
            "-dl": self.download,
            "-ls": self.list_bucket,
        }

    def upload(self, filePath: str, bucket: str = None, key: str = None):
        """
        上传文件

        Upload file

        :param filePath: 文件路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        import os
        from .. import dir_char

        filename = os.path.basename(filePath)

        def progress(cur, total):
            if not self.bar:
                from ..TuiTools.Bar import DataTransformBar

                self.bar = DataTransformBar()
                self.tid = self.bar.add_task(
                    "Transform" if user_lang != "zh" else "传输",
                    filename=filename,
                    total=total,
                )
                self.bar.start()
                self.bar.start_task(self.tid)
            self.bar.update(self.tid, completed=cur)

        filePath = filePath.strip()
        tk = self.auth.upload_token(bucket if bucket else self.df_bucket, filePath)
        QiniuOSS.qiniu.put_file(
            tk,
            key if key else filePath.replace(dir_char, "/"),
            filePath,
            progress_handler=progress,
        )
        self.bar.stop()

    def remove(self, filePath: str, bucket: str = None):
        """
        删除文件

        Delete file

        :param filePath: 文件路径（对象存储中）
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bk = QiniuOSS.qiniu.BucketManager(self.auth)
        bk.delete(bucket if bucket else self.df_bucket, filePath)

    def copy_url(self, filePath: str, bucket: str = None):
        """
        通过url拷贝文件（这个接口貌似没有卵用，七牛云那边并不会生效）

        Copy files through URL (this interface seems to have no egg use, qiniu cloud will not work)

        :param filePath: 文件链接
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bk = QiniuOSS.qiniu.BucketManager(self.auth)
        bk.fetch(
            filePath, bucket if bucket else self.df_bucket, filePath.split("/")[-1]
        )

    def get_bucket_url(self, bucket: str = None):
        """
        获取当前桶的访问链接

        Gets the access link for the current bucket

        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: 成功返回json，否则False
        """
        import requests

        bucket = bucket if bucket else self.df_bucket
        url = "http://api.qiniu.com/v6/domain/list?tbl=%s" % bucket
        res = requests.get(
            url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "QBox %s" % self.auth.token_of_request(url),
            },
        )
        if res.status_code == requests.codes.ok:
            return res.json()
        else:
            return False

    def list_bucket(self, bucket: str = None):
        """
        展示bucket中所有的文件

        Displays all the files in the bucket

        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from .. import qs_default_console, qs_info_string
        from ..TuiTools.Table import qs_default_table
        from rich.text import Text

        bk = QiniuOSS.qiniu.BucketManager(self.auth)
        ret = bk.list(bucket if bucket else self.df_bucket)
        if not ret[1]:
            print("ERROR!" if user_lang != "zh" else "错误!")
            exit(0)
        root_url = "http://" + self.get_bucket_url(bucket)[0] + "/"
        ret = ret[0]["items"]
        from ..NetTools.NormalDL import size_format

        tb = qs_default_table(
            ["File", "Size"] if user_lang != "zh" else ["文件", "体积"], title="七牛 OSS"
        )
        for i in ret:
            tb.add_row(
                Text(i["key"], justify="left"),
                Text(size_format(i["fsize"], True), justify="right"),
            )
        qs_default_console.print(
            qs_info_string, "Bucket url:" if user_lang != "zh" else "桶链接:", root_url
        )
        qs_default_console.print(tb, justify="center")

    def download(self, filePath: str, bucket: str = None):
        """
        下载文件

        Download file

        :param filePath: 文件在桶中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from ..NetTools.NormalDL import normal_dl

        bucket = bucket if bucket else self.df_bucket
        root_url = self.get_bucket_url(bucket)[0]
        if root_url:
            root_url = "http://" + root_url + "/"
        else:
            exit("Get Bucket Url Failed!" if user_lang != "zh" else "获取桶链接失败!")
        dl_url = root_url + filePath
        if bucket.startswith("admin"):
            dl_url = self.auth.private_download_url(dl_url)
        normal_dl(dl_url)
