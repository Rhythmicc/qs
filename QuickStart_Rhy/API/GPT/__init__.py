from ... import qs_config, requirePackage

_chatbot = None

def ChatGPT(prompt: str):
    global _chatbot

    if not _chatbot:
        _config = qs_config.basicSelect("gpt")
        api_supporter = _config["support"][_config["index"]]
        model = _config["model"]
        _chatbot = requirePackage('.API.GPT.' + api_supporter, 'create_bot')(model)
    
    return _chatbot.ask_stream(prompt)
