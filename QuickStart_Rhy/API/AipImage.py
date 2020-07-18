from QuickStart_Rhy.API import pre_check, os
try:
    import aip
except ImportError:
    exit('You need install: baidu-aip')
import base64


class ImageDeal:
    """
    百度图像处理类
    """
    def __init__(self, app_id=pre_check('AipImageAPP_ID'),
                 app_key=pre_check('AipImageAPP_KEY'),
                 secret_key=pre_check('AipImageSECRET_KEY')):
        """
        初始化并登陆百度图像处理

        :param app_id: 应用ID
        :param app_key: 应用key
        :param secret_key: 密钥
        """
        self.client = aip.AipImageProcess(app_id, app_key, secret_key)

    def largeImage(self, path):
        """
        放大图片 (图像效果增强)

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
            img = base64.b64decode(img['image'])
            with open(img_name, 'wb') as f:
                f.write(img)
        except :
            from pprint import pprint
            pprint(img)
