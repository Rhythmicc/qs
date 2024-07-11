from ... import qs_config, requirePackage

_chatbot = None

def save_conversation(filename: str):
    global _chatbot

    if _chatbot:
        _chatbot.save_conversation(filename)
    yield "Conversation saved to file: " + filename


cmd = {
    '/save': save_conversation
}


def empty_iterator():
    yield None

def ChatGPT(prompt: str, system_prompt: str = None, record_history=True, model=None):
    global _chatbot

    if not _chatbot:
        _config = qs_config.basicSelect("gpt")
        api_supporter = _config["index"]
        if not system_prompt:
            system_prompt = qs_config.basicSelect("gpt")["prompt"].items()[0][1]
        if not model:
            model = _config["model"]
        _chatbot = requirePackage(".API.GPT." + api_supporter, "create_bot")(
            model,
            system_prompt=system_prompt,
            record_history=record_history,
        )

    if prompt.startswith("/"):
        # parse command
        cmd_name, *args = prompt.split()
        if cmd_name in cmd:
            return cmd[cmd_name](' '.join(args))
        else:
            yield "Unknown command"

    return _chatbot.ask_stream(prompt)
