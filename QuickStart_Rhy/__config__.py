from prompt_toolkit.validation import Validator, ValidationError
from inquirer_rhy.prompt import prompt
import sys
from rich.console import Console

qs_default_console = Console()
system = sys.platform
if system.startswith('win'):
    dir_char = '\\'
else:
    dir_char = '/'


default_language = {
    'type': 'input',
    'name': 'default_language',
    'message': """Select your language, the flowing content is available choice
  选择你的语言，下述内容为合法选项 (此处顺序无任何意义)
    
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
                                    'slo', 'swe', 'hu', 'vie', 'Not Set | 暂不配置'],
    'default': 'Not Set | 暂不配置'
}

default_currency = {
    'type': 'input',
    'name': 'default_currency',
    'message': """Choose your common currency, the flowing content is available choice
  选择你常用的币种，下述内容为合法选项 (此处顺序无任何意义)
    
    CNY (Chinese)  USD (American) JPY (Japanese)  KRW (Korean)    DKK (Denmark)  EUR (Europe) 
    THB (Thailand) SAR (al-ummah) RUB (Russian)   BYR (Belarus)   RON (Romania)  PLN (Poland)
    BGN (Bulgaria) CZK (Czech)    ISK (Iceland)   VND (Vietnam)   DZD (Algeria)  ARS (Argentina)
    SEK (Sweden)   HUF (Hungary)  OMR (Amani)     AUD (Australia) MOP (Macao)    AED (United Arab Emirates)
    EGP (Egypt)    BHD (Bahrain)  BRL (Brazil)    HKD (HongKong)  COP (Colombia) PHP (Philippines)
    CAD (Canada)   KHR (Cambodia) QAR (Qatar)     HRK (Croatia)   KES (Kenya)    CRC (CostaRica)
    MXN (Mexico)   MAD (Morocco)  KWD (Kuwait)    LAK (Laos)      LBP (Lebanon)  MYR (Malaysia)
    BUK (Myanmar)  NOK (Norway)   SEK (Sweden)    RSD (Serbia)    TZS (Tanzania) ZAR (South Africa)
    BND (Brunei)   UGX (Uganda)   ZMK (Zambian)   SGD (Singapore) TWD (TaiWan)   LKR (Sri Lanka)  
    TRY (Turkey)   HUF (Hungary)  SYP (Syria)     IQD (Iraq)      INR (India)    NZD (New Zealand)
    GBP (England)  ILS (Israel)   JOD (Jordan)    CLP (Chile)     IDR (Indonesia)
    
  Input the default currency | 输入默认币种:""",
    'validate': lambda val: val in {'CLP', 'AED', 'CZK', 'THB', 'MYR', 'NZD', 'LBP', 'LAK', 'HUF', 'VND',
                                    'ZMK', 'RSD', 'CNH', 'BYR', 'HRK', 'CHF', 'CNY', 'TWD', 'CAD', 'RON',
                                    'MOP', 'CRC', 'COP', 'LKR', 'IDR', 'AUD', 'ARS', 'BGN', 'KRW', 'TZS',
                                    'JOD', 'HKD', 'EGP', 'KHR', 'ZAR', 'BRL', 'OMR', 'BHD', 'NOK', 'PLN',
                                    'QAR', 'RUB', 'MAD', 'EUR', 'GBP', 'BND', 'SAR', 'USD', 'KWD', 'SYP',
                                    'DKK', 'ILS', 'ISK', 'DZD', 'JPY', 'SEK', 'TRY', 'INR', 'KES', 'SGD',
                                    'UGX', 'PHP', 'IQD', 'BUK', 'MXN', 'Not set | 暂不设置'},
    'default': 'Not set | 暂不设置'
}

default_translate_engine = {
    'type': 'list',
    'name': 'default_translate_engine',
    'message': 'Select translate engine    | 选择翻译引擎:',
    'choices': ['default', 'TencentCloud']
}

default_pip = {
    'type': 'input',
    'name': 'default_pip',
    'message': 'Input the default pip | 输入默认pip:',
    'default': 'pip3'
}


force_show_img = {
    'type': 'confirm',
    'name': 'force_show_img',
    'message': 'Force show image in terminal | 强制在终端显示图片?',
    'default': False
}


class proxyValidator(Validator):
    from .NetTools import is_ip

    def validate(self, document):
        document = document.text
        if document == 'Not set | 暂不设置':
            return True
        ip_flag = proxyValidator.is_ip(':'.join(document.split('@')[-1].split(':')[:-1]))
        if not ip_flag:
            raise ValidationError(message='Not a valid IP address | 非合法ip地址', cursor_position=len(document))
        return False


default_proxy = {
    'type': 'input',
    'name': 'default_proxy',
    'message': 'Input download proxy       | 输入下载代理:',
    'default': 'Not set | 暂不设置',
    'validate': proxyValidator
}


class QsConfig:
    import json

    def __init__(self, configPath, isExists):
        self.path = configPath
        if isExists:
            try:
                with open(configPath, 'r') as f:
                    self.config = QsConfig.json.loads(f.read())
            except:
                with open(configPath, 'r', encoding='utf8') as f:
                    self.config = QsConfig.json.loads(f.read(), encoding='utf8')
        else:
            self.config = QsConfig.json.loads("""{
  "basic_settings": {
    "default_language": "zh",
    "default_currency": "CNY",
    "default_translate_engine": {
      "index": 0,
      "support": ["default", "TencentCloud"]
    },
    "default_proxy": "user:password@ip:port or ip:port",
    "default_pip": "pip3",
    "force_show_img": false
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
    "AipImageAPP_ID": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipImageAPP_KEY": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipImageSECRET_KEY": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipNlpAPP_ID" : "GET: https://cloud.baidu.com/product/nlp_apply",
    "AipNlpAPP_KEY": "GET: https://cloud.baidu.com/product/nlp_apply",
    "AipNlpSECRET_KEY": "GET: https://cloud.baidu.com/product/nlp_apply",
    "commonClipboardFilePath": "GET: /Path/to/file",
    "alapi_token": "GET: https://user.alapi.cn/",
    "lolicon_token": "GET: https://api.lolicon.app/#/setu?id=apikey"
  }
}""")
            res = prompt([default_language, default_currency, default_translate_engine, default_proxy, default_pip])
            self.config['basic_settings']['default_language'] = res['default_language'] if res['default_language'] != 'Not Set | 暂不配置' else 'en'
            self.config['basic_settings']['default_currency'] = res['default_currency'] if res['default_currency'] != 'Not Set | 暂不配置' else 'USD'
            self.config['basic_settings']['default_translate_engine']['index'] = ['default', 'TencentCloud'].index(
                res['default_translate_engine'])
            self.config['basic_settings']['default_proxy'] = "" if res['default_proxy'] == 'Not set | 暂不设置' else res[
                'default_proxy']
            self.config['basic_settings']['default_pip'] = res['default_pip']
            self.update()
            qs_default_console.print(
                '\nYour configuration table has been stored\n你的配置表被存储在: [bold green]' + '%s' % configPath + '[/bold green]')
            qs_default_console.print(
                '[bold red]\nqs will not use your configuration do anything!\nQpro不会用您的配置表做任何事情![/bold red]')
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
  the Mac system, whether to open the iTerm2 official website?
  qs推荐您在Mac系统中使用iTerm2作为终端程序, 是否打开iTerm2官网?""",
                'default': True})['use_iTerm']:
                from .NetTools import open_url
                open_url('https://www.iterm2.com/')

    def update(self):
        with open(self.path, 'w') as f:
            QsConfig.json.dump(self.config, f, indent=4, separators=(',', ': '))

    def basicSelect(self, key: str):
        if key not in self.config['basic_settings']:
            exec(f'res = prompt([{key}])')
            exec(f"self.config['basic_settings']['{key}'] = res['{key}']")
            self.update()
        return self.config['basic_settings'][key]

    def apiSelect(self, key):
        if key not in self.config['API_settings']:
            raise KeyError
        return self.config['API_settings'][key]

    def basicUpdate(self, key: str, value: str):
        self.config['basic_settings'][key] = value
        return self.update()

    def apiUpdate(self, key: str, value: str):
        self.config['API_settings'][key] = value
        return self.update()
