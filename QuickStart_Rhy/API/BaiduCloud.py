# coding=utf-8
from QuickStart_Rhy.API import *
try:
    import aip
except ImportError:
    exit('You need install: baidu-aip')


class ImageDeal:
    """
    百度图像处理类

    Baidu image processing class
    """
    import base64

    def __init__(self, app_id=pre_check('AipImageAPP_ID'),
                 app_key=pre_check('AipImageAPP_KEY'),
                 secret_key=pre_check('AipImageSECRET_KEY')):
        """
        初始化并登陆百度图像处理

        Initialize and log in Baidu image processing

        :param app_id: 应用ID
        :param app_key: 应用key
        :param secret_key: 密钥
        """
        self.client = aip.AipImageProcess(app_id, app_key, secret_key)

    def largeImage(self, path):
        """
        放大图片 (图像效果增强)

        Enlarge image (Image Enhancement)

        :param path: 图片路径
        :return: None
        """
        if not os.path.exists(path) or not os.path.isfile(path):
            print('No file named: %s' % path)
            return
        img_name = os.path.basename(path)
        img_name = img_name[:img_name.index('.')] + '_LG.' + '.'.join(img_name.split('.')[1:])
        with open(path, 'rb') as f:
            img = f.read()
        img = self.client.imageQualityEnhance(img)
        try:
            img = ImageDeal.base64.b64decode(img['image'])
            with open(img_name, 'wb') as f:
                f.write(img)
        except :
            from pprint import pprint
            pprint(img)


class AipNLP:
    """
    百度语言处理类

    Baidu language processing class
    """
    def __init__(self,
                 appid=pre_check("AipNlpAPP_ID"),
                 appkey=pre_check("AipNlpAPP_KEY"),
                 sckey=pre_check("AipNlpSECRET_KEY")):
        """
        初始化并登陆百度语言处理应用

        Initialize and log in baidu language processing application

        :param appid: 应用ID
        :param appkey: 应用Key
        :param sckey: 密钥
        """
        self.client = aip.AipNlp(appid, appkey, sckey)

    def get_res(self, words):
        """
        文本纠错

        Text error correction

        :param words: 待处理文本
        :return: 处理后的文本 | proceed words
        """
        try:
            res = self.client.ecnet(words)['item']['correct_query']
        except Exception as e:
            exit(repr(e))
        else:
            return res
