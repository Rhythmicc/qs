from QuickStart_Rhy.API import pre_check
try:
    import aip
except ImportError:
    exit('You need install: baidu-aip')


class AipNLP:
    def __init__(self, 
                 appid=pre_check("AipNlpAPP_ID"),
                 appkey=pre_check("AipNlpAPP_KEY"),
                 sckey=pre_check("AipNlpSECRET_KEY")):
        self.client = aip.AipNlp(appid, appkey, sckey)

    def get_res(self, words):
        try:
            res = self.client.ecnet(words)['item']['correct_query']
        except Exception as e:
            exit(repr(e))
        else:
            return res
