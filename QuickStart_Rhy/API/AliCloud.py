# coding=utf-8
"""
阿里云相关API

Alibaba cloud API
"""
from . import pre_check, user_lang, dir_char
from .. import requirePackage
oss2 = requirePackage('oss2')


class AliyunOSS:
    def __init__(self, ac_id=pre_check('aliyun_oss_acid'), ac_key=pre_check('aliyun_oss_ackey'),
                 bucket_url=pre_check('aliyun_oss_df_endpoint'), df_bucket=pre_check('aliyun_oss_df_bucket')):
        """
        初始化并登陆阿里云对象存储

        Initializes and logs into ali cloud object storage

        :param ac_id: Access id
        :param ac_key: Access key
        :param bucket_url: oss-[地区 | location].aliyuncs.com
        :param df_bucket: 桶名称
        """
        self.ac_id = ac_id
        self.ac_key = ac_key
        self.bucket_url = bucket_url
        self.df_bucket = df_bucket
        self.progress, self.trans_id, self._progress_file_name = None, None, None
        self.auth = oss2.Auth(self.ac_id, self.ac_key)

    def get_func_table(self):
        """
        获取OSS类支持的操作

        Get the operations supported by the OSS class

        :return: 支持的函数字典
        """
        return {
            '-up': self.upload,
            '-rm': self.remove,
            '-dl': self.download,
            '-ls': self.list_bucket
        }

    def _progress_bar(self, cur, total):
        """
        创建一个进度条并启动

        Create a progress bar and start

        :param cur: 当前完成量
        :param total: 总任务量
        :return: None
        """
        if not self.progress:
            from ..TuiTools.Bar import DataTransformBar
            self.progress = DataTransformBar(True if total else False)
            self.trans_id = self.progress.add_task('Transform', total=total if total else -1,
                                                   filename=self._progress_file_name)
            self.progress.start()
            self.progress.start_task(self.trans_id)
        self.progress.update(self.trans_id, completed=cur)

    def upload(self, filePath: str, bucket: str = None):
        """
        上传文件（支持断点续传）

        Upload file (support breakpoint continuation)

        :param filePath: 文件路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        import os
        from .. import qs_default_console, qs_info_string
        from ..SystemTools import get_core_num
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        filePath = filePath.strip()
        self._progress_file_name = os.path.basename(filePath)
        oss2.resumable_upload(bucket, filePath.replace(dir_char, '/'), filePath, num_threads=get_core_num() * 4,
                              progress_callback=self._progress_bar)
        self.progress.stop()
        qs_default_console.print(qs_info_string, 'Transform Completed!' if user_lang != 'zh' else '传输完成!')

    def download(self, filename: str, bucket: str = None):
        """
        下载文件（支持断点续传）

        Download file (support breakpoint continuation)

        :param filename: 文件在bucket中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        import os
        from .. import qs_default_console, qs_info_string
        from ..SystemTools import get_core_num
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        self._progress_file_name = os.path.basename(filename)
        oss2.resumable_download(bucket, filename, filename, num_threads=get_core_num() * 4,
                                progress_callback=self._progress_bar)
        self.progress.stop()
        qs_default_console.print(qs_info_string, 'Transform Completed!' if user_lang != 'zh' else '传输完成!')

    def remove(self, filePath: str, bucket: str = None):
        """
        删除文件

        delete file

        :param filePath: 文件在bucket中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        bucket.delete_object(filePath)

    def list_bucket(self, bucket: str = None):
        """
        打印桶中的文件表

        Print the file table in the bucket

        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from .. import qs_default_console, qs_info_string
        from ..NetTools.NormalDL import size_format
        from ..TuiTools.Table import qs_default_table
        from rich.text import Text

        bucket = bucket if bucket else self.df_bucket
        ls = oss2.Bucket(self.auth, self.bucket_url, bucket)
        tb = qs_default_table(['File', 'Size'] if user_lang != 'zh' else ['文件', '体积'], title='Aliyun OSS')
        prefix = dict()
        for obj in oss2.ObjectIterator(ls):
            if '/' in obj.key:
                prefix[obj.key[obj.key[:obj.key.index('/')]]] = 0
            tb.add_row(Text(obj.key, justify='left'), Text(size_format(obj.size, True), justify='right'))
        qs_default_console.print(
            qs_info_string,
            'Bucket Url:' if user_lang != 'zh' else '桶链接:',
            'https://' + bucket + '.' + self.bucket_url + '/'
        )
        qs_default_console.print(tb, justify="center")
