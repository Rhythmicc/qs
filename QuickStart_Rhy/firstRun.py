# coding=utf-8
"""
第一次运行qs

Running QS for the first time
"""
import json
import colorama
from colorama import Fore, Style
from PyInquirer import prompt
from . import user_root, system
from .NetTools import is_ip
from prompt_toolkit.validation import Validator, ValidationError


colorama.init()


class proxyValidator(Validator):
    def validate(self, document):
        document = document.text
        if document == 'Not set | 暂不设置':
            return True
        ip_flag = is_ip(':'.join(document.split('@')[-1].split(':')[:-1]))
        if not ip_flag:
            raise ValidationError(message='Not a valid IP address | 非合法ip地址', cursor_position=len(document))
        return False


def main(rt_dir: str) -> dict:
    """
    初始化qs配置文件

    Initialize the qs configuration file

    :param rt_dir:
    :return:
    """
    questions = [{
        'type': 'input',
        'name': 'default_language',
        'message': """Select your language, the flowing content is available choice
  选择你的语言，下述内容为合法选项
    
    zh  (Chinese) en  (English)  jp  (Japanese) kor (Korean)   fra (French), 
    spa (Spanish) th  (Thailand) ara (al-ummah) ru  (Russian)  pt  (Portuguese), 
    de  (Germany) it  (Italy)    el  (Greece)   nl  (Poland)   bul (Bulgaria),
    est (Estonia) dan (Denmark)  fin (Finland)  cs  (Czech)    rom (Romania),
    slo (Iceland) swe (Sweden)   hu  (Hungary)  vie (Vietnam)
    
  Input the default language | 输入默认语言:""",
        'validate': lambda val: val in ['zh', 'en', 'jp', 'kor', 'fra',
                                        'spa', 'th', 'ara', 'ru', 'pt',
                                        'de', 'it', 'el', 'nl', 'bul',
                                        'est', 'dan', 'fin', 'cs', 'rom',
                                        'slo', 'swe', 'hu', 'vie']
    }, {
        'type': 'list',
        'name': 'default_translate_engine',
        'message': 'Select translate engine    | 选择翻译引擎:',
        'choices': ['default', 'TencentCloud']
    }, {
        'type': 'input',
        'name': 'default_proxy',
        'message': 'Input download proxy       | 输入下载代理:',
        'default': 'Not set | 暂不设置',
        'validate': proxyValidator
    }]
    config = json.loads("""{
  "basic_settings": {
    "default_language": "zh",
    "default_translate_engine": {
      "index": 0,
      "support": ["default", "TencentCloud"]
    },
    "default_proxy": "user:password@ip:port or ip:port"
  },
  "API_settings": {
    "rmbg": "GET: https://www.remove.bg",
    "smms": "GET: https://sm.ms",
    "darksky": "GET: https://darksky.net/",
    "aliyun_oss_acid": "GET: https://www.aliyun.com/product/oss",
    "aliyun_oss_ackey": "GET: https://www.aliyun.com/product/oss",
    "aliyun_oss_bucket_url": "GET: https://www.aliyun.com/product/oss",
    "aliyun_oss_df_bucket": "GET: https://www.aliyun.com/product/oss",
    "txyun_scid": "GET: https://console.cloud.tencent.com/",
    "txyun_sckey": "GET: https://console.cloud.tencent.com/",
    "txyun_cos_df_bucket": "GET: https://console.cloud.tencent.com/",
    "txyun_df_region": "GET: ap-[location]",
    "qiniu_ac_key": "GET: http://qiniu.com/",
    "qiniu_sc_key": "GET: http://qiniu.com/",
    "qiniu_bk_name": "GET: [Qiniu Bucket Name]",
    "gitee": "GET: http://gitee.com/",
    "ipinfo": "GET: https://ipinfo.io/",
    "AipImageAPP_ID": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipImageAPP_KEY": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipImageSECRET_KEY": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipNlpAPP_ID" : "GET: https://cloud.baidu.com/product/nlp_apply",
    "AipNlpAPP_KEY": "GET: https://cloud.baidu.com/product/nlp_apply",
    "AipNlpSECRET_KEY": "GET: https://cloud.baidu.com/product/nlp_apply",
    "commonClipboardFilePath": "GET: /Path/to/file",
    "alapi_token": "GET: https://user.alapi.cn/"
  }
}
""")
    res = prompt(questions)
    config['basic_settings']['default_language'] = res['default_language']
    config['basic_settings']['default_translate_engine']['index'] = ['default', 'TencentCloud'].index(res['default_translate_engine'])
    config['basic_settings']['default_proxy'] = "" if res['default_proxy'] == 'Not set | 暂不设置' else res['default_proxy']
    with open(rt_dir + '.qsrc', 'w') as f:
        json.dump(config, f, indent=4, separators=(',', ': '))
        print('\nYour configuration table has been stored\n你的配置表被存储在: ' + Fore.LIGHTGREEN_EX + '%s' % (rt_dir + '.qsrc') + Style.RESET_ALL)
        prompt({
            'type': 'confirm',
            'message': 'Confirm | 确认',
            'name': 'done',
            'default': True
        })
    if system.startswith('darwin') and prompt({
            'type': 'confirm',
            'name': 'use_iTerm',
            'message': """Qs recommends that you use iTerm as the terminal program in
  the Mac system, whether to open the iTerm official website?
  qs推荐您在Mac系统中使用iTerm作为终端程序, 是否打开iTerm官网?""",
            'default': True})['use_iTerm']:
        from .NetTools import open_url
        open_url('https://www.iterm2.com/')

    return config


if __name__ == "__main__":
    main(user_root)
