import json
from QuickStart_Rhy.API import pre_check
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tmt.v20180321 import tmt_client, models


class Translate:
    def __init__(self, scid=pre_check('txyun_scid'), sckey=pre_check('txyun_sckey'), region=pre_check('txyun_df_region')):
        cred = credential.Credential(scid, sckey)
        http_profile = HttpProfile()
        http_profile.endpoint = "tmt.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = http_profile
        self.client = tmt_client.TmtClient(cred, region, clientProfile)

    def langdetect(self, text):
        req = models.LanguageDetectRequest()
        req.from_json_string(json.dumps({
            "Text": text,
            "ProjectId": 0
        }))
        return json.loads(self.client.LanguageDetect(req).to_json_string())['Lang']

    def translate(self, text: str):
        req = models.TextTranslateRequest()
        req.from_json_string(json.dumps({
            "SourceText": text,
            "Source": self.langdetect(text),
            "Target": "zh",
            "ProjectId": 0
        }))
        return json.loads(self.client.TextTranslate(req).to_json_string())['TargetText']

