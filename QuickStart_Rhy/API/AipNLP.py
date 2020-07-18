from QuickStart_Rhy.API import pre_check
try:
    import aip
except ImportError:
    exit('You need install: baidu-aip')


class AipNLP:
    """
    百度语言处理类
    """
    def __init__(self, 
                 appid=pre_check("AipNlpAPP_ID"),
                 appkey=pre_check("AipNlpAPP_KEY"),
                 sckey=pre_check("AipNlpSECRET_KEY")):
        """
        初始化并登陆百度语言处理应用

        :param appid: 应用ID
        :param appkey: 应用Key
        :param sckey: 密钥
        """
        self.client = aip.AipNlp(appid, appkey, sckey)

    def get_res(self, words):
        """
        文本纠错

        :param words: 待处理文本
        :return: 处理后的文本
        """
        try:
            res = self.client.ecnet(words)['item']['correct_query']
        except Exception as e:
            exit(repr(e))
        else:
            return res
