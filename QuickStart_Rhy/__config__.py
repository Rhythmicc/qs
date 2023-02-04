from QuickProject import QproDefaultConsole as qs_default_console
from QuickProject import _ask, user_lang
import sys
import os


platform = sys.platform
if platform.startswith("win"):
    dir_char = "\\"
else:
    dir_char = "/"


translate_engines = ["default", "TencentCloud", "DeepL"]

questions = {
    "default_currency": {
        "type": "input",
        "name": "default_currency",
        "message": (
            "Choose your common currency, the flowing content is available choice (the order is meaningless)"
            if user_lang != "zh"
            else "选择你常用的币种，下述内容为合法选项 (此处顺序无任何意义)"
        )
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
        + ("Input the default currency" if user_lang != "zh" else "输入默认币种"),
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
        "message": "Select translate engine" if user_lang != "zh" else "选择翻译引擎",
        "choices": translate_engines,
        "default": "default",
    },
    "force_show_img": {
        "type": "confirm",
        "name": "force_show_img",
        "message": "Force show image in terminal" if user_lang != "zh" else "强制在终端显示图片",
        "default": False,
    },
    "default_proxy": {
        "type": "input",
        "name": "default_proxy",
        "message": "Input download proxy" if user_lang != "zh" else "输入下载代理",
        "default": "Not set | 暂不设置",
    },
    "terminal_font_size": {
        "type": "input",
        "name": "terminal_font_size",
        "message": "Input terminal font size" if user_lang != "zh" else "输入终端字体大小",
        "default": "16",
    },
}


class QsConfig:
    import json

    def __init__(self, configPath):
        self.path = configPath
        if os.path.exists(configPath):
            try:
                with open(configPath, "r") as f:
                    self.config = QsConfig.json.loads(f.read())
            except:
                with open(configPath, "r", encoding="utf8") as f:
                    self.config = QsConfig.json.loads(f.read(), encoding="utf8")
        else:
            self.config = QsConfig.json.loads(
                """{
  "basic_settings": {
    "default_language": "zh",
    "default_currency": "CNY",
    "default_translate_engine": {
      "index": 0,
      "support": ["default", "TencentCloud", "DeepL"]
    },
    "default_proxy": "user:password@ip:port or ip:port",
    "default_pip": "pip3",
    "force_show_img": false,
    "terminal_font_size": 16
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
    "lolicon_token": "GET: https://api.lolicon.app/#/setu?id=apikey",
    "openai": "GET: https://openai.com/api/",
    "DeepL": "GET: https://www.deepl.com/zh/pro-api?cta=header-pro-api/"
  }
}"""
            )
            from QuickProject import user_lang, user_pip

            self.config["basic_settings"]["default_language"] = user_lang
            self.config["basic_settings"]["default_currency"] = _ask(
                questions["default_currency"]
            )
            self.config["basic_settings"]["default_translate_engine"][
                "index"
            ] = translate_engines.index(_ask(questions["default_translate_engine"]))
            self.config["basic_settings"]["default_proxy"] = _ask(
                questions["default_proxy"]
            )
            self.config["basic_settings"]["default_pip"] = user_pip
            self.update()
            qs_default_console.print(
                "\nYour configuration table has been stored:"
                if user_lang != "zh"
                else "\n你的配置表被存储在:",
                f"[bold green]{configPath}[/bold green]",
            )
            # qs_default_console.print(
            #     "[bold red]\nqs will not use your configuration do anything!\nQpro不会用您的配置表做任何事情![/bold red]"
            # )
            qs_default_console.print(
                "[bold red]\nqs will not use your configuration do anything![/bold red]"
                if user_lang != "zh"
                else "[bold red]\nQpro不会用您的配置表做任何事情![/bold red]"
            )
            _ask(
                {
                    "type": "confirm",
                    "message": "Confirm | 确认",
                    "default": True,
                }
            )
            if platform.startswith("darwin") and _ask(
                {
                    "type": "confirm",
                    "message": """Qs recommends that you use iTerm as the terminal program in
  the Mac system, whether to open the iTerm2 official website?"""
                    if user_lang != "zh"
                    else "qs推荐您在Mac系统中使用iTerm2作为终端程序, 是否打开iTerm2官网?",
                    "default": True,
                }
            ):
                from .NetTools import open_url

                open_url("https://www.iterm2.com/")

    def update(self):
        with open(self.path, "w") as f:
            QsConfig.json.dump(self.config, f, indent=4, separators=(",", ": "))

    def basicSelect(self, key: str):
        if key not in self.config["basic_settings"]:
            self.config["basic_settings"][key] = _ask(questions[key])
            self.update()
        return self.config["basic_settings"][key]

    def apiSelect(self, key):
        if key not in self.config["API_settings"]:
            raise KeyError
        return self.config["API_settings"].get(key, None)

    def basicUpdate(self, key: str, value: str):
        self.config["basic_settings"][key] = value
        return self.update()

    def apiUpdate(self, key: str, value: str):
        self.config["API_settings"][key] = value
        return self.update()
