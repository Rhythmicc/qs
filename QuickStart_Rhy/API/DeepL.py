"""
DeepL 翻译 API
"""

from . import pre_check
from .. import user_lang, requirePackage


_translator = requirePackage("deepl", "Translator")(pre_check("DeepL"))  # 持久翻译复用


def translate(text, target_lang=user_lang.lower()):
    """翻译文本"""
    return _translator.translate_text(text, target_lang=target_lang).text


if __name__ == "__main__":
    print(translate("Hello World!"))
