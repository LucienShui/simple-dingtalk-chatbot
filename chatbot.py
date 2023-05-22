from requests.api import post
import time
from urllib.parse import urljoin
from typing import Dict
from util import logger
from json import dumps
from functools import partial

dumps = partial(dumps, separators=(',', ':'), ensure_ascii=False)


class ChatBotBase:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)

    def chat(self, query: str, history: list = None, system: str = None) -> str:
        raise NotImplementedError

    def process(self, body: dict) -> dict:
        sender_id: str = body['senderId']
        content: str = body['text']['content']
        session_webhook: str = body['sessionWebhook']
        message_id: str = body['msgId']

        json_response = {
            "msgtype": "text",
            "text": {
                "content": self.chat(content)
            },
            "originalMsgId": message_id,
            "at": {
                "atMobiles": [],
                "atDingtalkIds": [sender_id],
                "isAtAll": False
            }
        }

        json_response = post(session_webhook, json=json_response).json()
        return json_response


class ChatGPT(ChatBotBase):
    def __init__(self, api_key: str, endpoint: str = 'https://api.openai-proxy.com',
                 model: str = "gpt-3.5-turbo", organization: str = None):
        super().__init__()
        self.model_list: list = ["gpt-4-0314", "gpt-4", "gpt-3.5-turbo-0301", "gpt-3.5-turbo"]
        assert model in self.model_list
        self.api_key: str = api_key
        self.url: str = urljoin(endpoint, '/v1/chat/completions')
        self.model: str = model
        self.headers = {'Authorization': f'Bearer {self.api_key}', 'OpenAI-Organization': organization}

    def chat(self, query: str, history: list = None, system: str = None) -> str:
        history = history or []
        messages: list = [{'role': 'system', 'content': system}] if system else []
        for q, a in history:
            messages.append({"role": "user", "content": q})
            messages.append({"role": "assistant", "content": a})
        messages.append({"role": "user", "content": query})
        request: dict = {"model": self.model, "messages": messages}
        start_time = time.time()
        response: dict = post(self.url, json=request, headers=self.headers).json()
        duration = time.time() - start_time
        log_msg = f"request = {dumps(request)}, response = {dumps(response)}, cost = {round(duration * 1000, 2)} ms"
        self.logger.info(log_msg)
        message: str = response['choices'].pop(0)['message']['content']
        return message


def from_config(bot_class: str, config: dict) -> ChatBotBase:
    supported_class = ['chatgpt']
    assert bot_class in supported_class
    if bot_class in 'chatgpt':
        return ChatGPT(**config)


def from_bot_map_config(bot_map_config: Dict[str, dict]) -> Dict[str, ChatBotBase]:
    bot_map: Dict[str, ChatBotBase] = {}
    for bot, config in bot_map_config.items():
        bot_class = config.pop('class')
        bot_map[bot] = from_config(bot_class, config)
    return bot_map
