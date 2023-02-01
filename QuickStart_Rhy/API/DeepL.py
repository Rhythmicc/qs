"""
DeepL 翻译 API
"""

from . import pre_check
from .. import user_lang, requirePackage


_token = pre_check("DeepL")
_translator = None  # 持久翻译复用


def translate(text, target_lang=user_lang.upper()):
    """翻译文本"""
    global _translator
    if not _translator:
        _translator = requirePackage("deepl", "Translator")(_token)
    return _translator.translate_text(text, target_lang=target_lang).text
