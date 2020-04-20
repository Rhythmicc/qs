from QuickStart_Rhy.API import pre_check, os
try:
    import aip
except ImportError:
    exit('You need install: baidu-aip')
import base64


class ImageDeal:
    def __init__(self, app_id=pre_check('AipImageAPP_ID'),
                 app_key=pre_check('AipImageAPP_KEY'),
                 secret_key=pre_check('AipImageSECRET_KEY')):
        self.client = aip.AipImageProcess(app_id, app_key, secret_key)

    def largeImage(self, path):
        if not os.path.exists(path) or not os.path.isfile(path):
            print('No file named: %s' % path)
            return
        img_name = os.path.basename(path)
        img_name = img_name[:img_name.index('.')] + '_LG.' + '.'.join(img_name.split('.')[1:])
        with open(path, 'rb') as f:
            img = f.read()
        img = self.client.imageQualityEnhance(img)['image']
        img = base64.b64decode(img)
        with open(img_name, 'wb') as f:
            f.write(img)
