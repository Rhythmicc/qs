from .. import requirePackage
from . import pre_check
import requests
import json

ENGINE = "gpt-3.5-turbo"
ENCODER = requirePackage("tiktoken", "get_encoding")("gpt2")
API_KEY = pre_check("openai")

class Chatbot:
    """
    Official ChatGPT API
    """

    def __init__(
        self,
        api_key: str = API_KEY,
        engine: str = ENGINE,
        proxy: str = None,
        max_tokens: int = 3000,
        temperature: float = 0.5,
        top_p: float = 1.0,
        reply_count: int = 1,
        system_prompt: str = "You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",
    ) -> None:
        """
        Initialize Chatbot with API key (from https://platform.openai.com/account/api-keys)
        """
        self.engine = engine
        self.session = requests.Session()
        self.api_key = api_key
        self.proxy = proxy
        if self.proxy:
            proxies = {
                "http": self.proxy,
                "https": self.proxy,
            }
            self.session.proxies = proxies
        self.conversation: list = [
            {
                "role": "system",
                "content": system_prompt,
            },
        ]
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.reply_count = reply_count

        initial_conversation = "\n".join([x["content"] for x in self.conversation])
        if len(ENCODER.encode(initial_conversation)) > self.max_tokens:
            raise Exception("System prompt is too long")

    def __add_to_conversation(self, message: str, role: str):
        """
        Add a message to the conversation
        """
        self.conversation.append({"role": role, "content": message})

    def __truncate_conversation(self):
        """
        Truncate the conversation
        """
        while True:
            full_conversation = "\n".join([x["content"] for x in self.conversation])
            if (
                len(ENCODER.encode(full_conversation)) > self.max_tokens
                and len(self.conversation) > 1
            ):
                # Don't remove the first message
                self.conversation.pop(1)
            else:
                break

    def ask_stream(self, prompt: str, role: str = "user", **kwargs) -> str:
        """
        Ask a question
        """
        self.__add_to_conversation(prompt, "user")
        self.__truncate_conversation()
        # Get response
        response = self.session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {kwargs.get('api_key', self.api_key)}"},
            json={
                "model": self.engine,
                "messages": self.conversation,
                "stream": True,
                # kwargs
                "temperature": kwargs.get("temperature", self.temperature),
                "top_p": kwargs.get("top_p", self.top_p),
                "n": kwargs.get("n", self.reply_count),
                "user": role,
            },
            stream=True,
        )
        if response.status_code != 200:
            raise Exception(
                f"Error: {response.status_code} {response.reason} {response.text}",
            )
        response_role: str = None
        full_response: str = ""
        for line in response.iter_lines():
            if not line:
                continue
            # Remove "data: "
            line = line.decode("utf-8")[6:]
            if line == "[DONE]":
                break
            resp: dict = json.loads(line)
            choices = resp.get("choices")
            if not choices:
                continue
            delta = choices[0].get("delta")
            if not delta:
                continue
            if "role" in delta:
                response_role = delta["role"]
            if "content" in delta:
                content = delta["content"]
                full_response += content
                yield content
        self.__add_to_conversation(full_response, response_role)

    def ask(self, prompt: str, role: str = "user", **kwargs):
        """
        Non-streaming ask
        """
        response = self.ask_stream(prompt, role, **kwargs)
        full_response: str = "".join(response)
        return full_response

    def rollback(self, n: int = 1):
        """
        Rollback the conversation
        """
        for _ in range(n):
            self.conversation.pop()

    def reset(self):
        """
        Reset the conversation
        """
        self.conversation = [
            {"role": "system", "content": self.system_prompt},
        ]

    def save(self, file: str):
        """
        Save the conversation to a JSON file
        """
        try:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(self.conversation, f, indent=2)
        except FileNotFoundError:
            print(f"Error: {file} cannot be created")

    def load(self, file: str):
        """
        Load the conversation from a JSON  file
        """
        try:
            with open(file, encoding="utf-8") as f:
                self.conversation = json.load(f)
        except FileNotFoundError:
            print(f"Error: {file} does not exist")


_chatbot = None


def chatGPT(
    prompt: str,
    wait_all: bool = False,
):
    """
    使用OpenAI的GPT-3 API进行聊天

    :param prompt: 聊天内容
    :param wait_all: 是否等待所有内容
    """
    global _chatbot
    if _chatbot is None:
        _chatbot = Chatbot()
    if wait_all:
        return _chatbot.ask(prompt)
    else:
        return _chatbot.ask_stream(prompt)
