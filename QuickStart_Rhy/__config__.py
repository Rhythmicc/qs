from QuickProject import QproDefaultConsole as qs_default_console
from QuickProject import _ask, user_lang
from langsrc import LanguageDetector
import json
import sys
import os


platform = sys.platform
if platform.startswith("win"):
    dir_char = "\\"
else:
    dir_char = "/"


translate_engines = ["default", "TencentCloud", "DeepL", "DeepLX"]
lang_detector = LanguageDetector(user_lang, os.path.join(os.path.dirname(__file__), "lang.json"))

questions = {
    "default_currency": {
        "type": "input",
        "name": "default_currency",
        "message": lang_detector['ask_default_currency']
        + """

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
    
  """
        + lang_detector['input_default_currency'],
        "validate": lambda val: val
        in {
            "CLP",
            "AED",
            "CZK",
            "THB",
            "MYR",
            "NZD",
            "LBP",
            "LAK",
            "HUF",
            "VND",
            "ZMK",
            "RSD",
            "CNH",
            "BYR",
            "HRK",
            "CHF",
            "CNY",
            "TWD",
            "CAD",
            "RON",
            "MOP",
            "CRC",
            "COP",
            "LKR",
            "IDR",
            "AUD",
            "ARS",
            "BGN",
            "KRW",
            "TZS",
            "JOD",
            "HKD",
            "EGP",
            "KHR",
            "ZAR",
            "BRL",
            "OMR",
            "BHD",
            "NOK",
            "PLN",
            "QAR",
            "RUB",
            "MAD",
            "EUR",
            "GBP",
            "BND",
            "SAR",
            "USD",
            "KWD",
            "SYP",
            "DKK",
            "ILS",
            "ISK",
            "DZD",
            "JPY",
            "SEK",
            "TRY",
            "INR",
            "KES",
            "SGD",
            "UGX",
            "PHP",
            "IQD",
            "BUK",
            "MXN",
        },
        "default": "USD",
    },
    "default_translate_engine": {
        "type": "list",
        "message": lang_detector['ask_translate_engine'],
        "choices": translate_engines,
        "default": "default",
    },
    "force_show_img": {
        "type": "confirm",
        "name": "force_show_img",
        "message": lang_detector['ask_force_show_img'],
        "default": "ITERM_SESSION_ID" in os.environ,
    },
    "default_proxy": {
        "type": "input",
        "name": "default_proxy",
        "message": lang_detector['ask_proxy'],
        "default": "Not set | 暂不设置",
    },
    "terminal_font_size": {
        "type": "input",
        "name": "terminal_font_size",
        "message": lang_detector['ask_font_size'],
        "default": "16",
    },
    "gpt": {
        "type": "list",
        "message": lang_detector['ask_gpt'],
        "choices": ["openai", "poe", "alapi"],
    },
    "gpt-model": {
        "type": "input",
        "message": lang_detector['ask_gpt_model']
    },
    "gpt-api": {
        "type": "input",
        "message": lang_detector['ask_gpt_api']
    },
    "gpt-url": {
        "type": "input",
        "message": lang_detector['ask_gpt_url']
    },
}


class QsConfig:
    def __init__(self, configPath):
        self.path = configPath
        if os.path.exists(configPath):
            try:
                with open(configPath, "r") as f:
                    self.config = json.loads(f.read())
            except:
                with open(configPath, "r", encoding="utf8") as f:
                    self.config = json.loads(f.read(), encoding="utf8")
        else:
            self.config = json.loads(
                """{
  "basic_settings": {
    "default_currency": "CNY",
    "default_translate_engine": {
      "index": 0,
      "support": ["default", "TencentCloud", "DeepL", "DeepLX", "AITranslate"]
    },
    "default_proxy": "user:password@ip:port or ip:port",
    "force_show_img": false,
    "terminal_font_size": 16,
    "terminal_font_rate": 2.049,
    "gpt": {
        "index": "openai",
        "support": {
            "openai": {
                "API_KEY": "",
                "API_URL": ""
            },
            "poe": "",
            "alapi": ""
        },
        "model": ""
    }
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
    "AipImageAPP_ID": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipImageAPP_KEY": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipImageSECRET_KEY": "GET: https://cloud.baidu.com/product/imageprocess",
    "AipNlpAPP_ID" : "GET: https://cloud.baidu.com/product/nlp_apply",
    "AipNlpAPP_KEY": "GET: https://cloud.baidu.com/product/nlp_apply",
    "AipNlpSECRET_KEY": "GET: https://cloud.baidu.com/product/nlp_apply",
    "alapi_token": "GET: https://user.alapi.cn/",
    "lolicon_token": "GET: https://api.lolicon.app/#/setu?id=apikey",
    "DeepL": "GET: https://www.deepl.com/zh/pro-api?cta=header-pro-api/",
    "DeepLX": "GET: https://github.com/OwO-Network/DeepLX"
  }
}"""
            )
            self.config["basic_settings"]["default_currency"] = _ask(
                questions["default_currency"]
            )
            self.config["basic_settings"]["default_translate_engine"][
                "index"
            ] = translate_engines.index(_ask(questions["default_translate_engine"]))
            self.config["basic_settings"]["default_proxy"] = _ask(
                questions["default_proxy"]
            )
            self.update()
            qs_default_console.print(
                "\n" + lang_detector['config_store_in'],
                f"[bold green]{configPath}[/bold green]",
            )
            _ask(
                {
                    "type": "confirm",
                    "message": lang_detector['confirm'],
                    "default": True,
                }
            )
            if (
                platform.startswith("darwin")
                and "ITERM_SESSION_ID" not in os.environ
                and _ask(
                    {
                        "type": "confirm",
                        "message": lang_detector['recommand_using_iterm2'],
                        "default": True,
                    }
                )
            ):
                from .NetTools import open_url

                open_url("https://www.iterm2.com/")

    def update(self):
        with open(self.path, "w") as f:
            json.dump(self.config, f, indent=4, separators=(",", ": "))

    def basicSelect(self, key: str, default=None):
        if key not in self.config["basic_settings"]:
            if default is not None:
                self.config["basic_settings"][key] = default
                self.update()
            elif key == 'gpt':
                _info = {
                    "index": _ask(questions['gpt']),
                    "support": {
                        "openai": {
                            "API_KEY": "",
                            "API_URL": ""
                        },
                        "poe": "",
                        "alapi": ""
                    },
                    "model": _ask(questions['gpt-model'])
                }
                if _info['index'] == 'openai':
                    _info['support']['openai']['API_KEY'] = _ask(questions['gpt-api'])
                    _info['support']['openai']['API_URL'] = _ask(questions['gpt-url'])
                else:
                    _info[_info['index']] = _ask(questions['gpt-api'])
                self.config["basic_settings"][key] = _info
                self.update()
            else:
                self.config["basic_settings"][key] = _ask(questions[key])
                self.update()
        return self.config["basic_settings"][key]

    def apiSelect(self, key):
        if key not in self.config["API_settings"]:
            raise KeyError
        return self.config["API_settings"].get(key, None)

    def basicUpdate(self, key: str, value):
        self.config["basic_settings"][key] = value
        return self.update()

    def apiUpdate(self, key: str, value: str):
        self.config["API_settings"][key] = value
        return self.update()
