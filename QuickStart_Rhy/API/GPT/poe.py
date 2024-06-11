from ... import requirePackage, user_lang, qs_config
from .common import GPTBotBase

API_KEY = qs_config.basicSelect("gpt")["support"].get("poe", None)
if not API_KEY:
    raise RuntimeError("No API key for POE Chatbot.")

import asyncio
import queue
import concurrent

get_bot_response = requirePackage(
    "fastapi_poe.client", "get_bot_response", real_name="fastapi-poe"
)
ProtocolMessage = requirePackage(
    "fastapi_poe.types", "ProtocolMessage", real_name="fastapi-poe"
)


lang_table = {
    "zh": "Chinese",
    "en": "English",
    "fra": "French",
    "ru": "Russian",
    "spa": "Spanish",
    "ara": "Arabic",
}


class AsyncToSyncIterator:
    def __init__(self, async_gen):
        self.queue = queue.Queue(maxsize=1)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        def run():
            async def _run():
                try:
                    async for item in async_gen:
                        self.queue.put(item)
                finally:
                    self.queue.put(StopIteration)

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_run())
            loop.close()

        self.executor.submit(run)

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration:
            raise StopIteration
        return item


class POEChatbot:
    def __init__(self, model, system_prompt, record_history=True):
        self.model = model
        self.messages = [ProtocolMessage(role="system", content=system_prompt)]
        self.record_history = record_history

    async def _ask_stream(self, prompt):
        self.messages.append(ProtocolMessage(role="user", content=prompt))
        if len(self.messages) > 4096:
            self.messages.pop(0)
        total_res = ""
        async for res in get_bot_response(
            self.messages, bot_name=self.model, api_key=API_KEY
        ):
            total_res += res.text
            yield total_res
        if self.record_history:
            self.messages.append(ProtocolMessage(role="bot", content=total_res))

    def ask_stream(self, prompt):
        return AsyncToSyncIterator(self._ask_stream(prompt))


def create_bot(
    model: str,
    system_prompt: str = f"You are ChatGPT, a large language model trained by OpenAI. Respond conversationally with Markdown format and using {lang_table[user_lang]} Language.",
    record_history=True
):
    return POEChatbot(model, system_prompt, record_history)
