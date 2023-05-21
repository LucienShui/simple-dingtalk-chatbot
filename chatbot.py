from requests.api import post
from json import load
from urllib.parse import urljoin
from typing import Dict


class ChatBotBase:
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
    def __init__(self, api_key: str, endpoint: str = 'https://api.openai-proxy.com', model: str = "gpt-3.5-turbo"):
        self.model_list: list = ["gpt-4-0314", "gpt-4", "gpt-3.5-turbo-0301", "gpt-3.5-turbo"]
        assert model in self.model_list
        self.api_key: str = api_key
        self.url: str = urljoin(endpoint, '/v1/chat/completions')
        self.model: str = model
        self.headers = {'Authorization': f'Bearer {self.api_key}'}

    def chat(self, query: str, history: list = None, system: str = None) -> str:
        history = history or []
        messages: list = [{'role': 'system', 'content': system}] if system else []
        for q, a in history:
            messages.append({"role": "user", "content": q})
            messages.append({"role": "assistant", "content": a})
        messages.append({"role": "user", "content": query})
        response = post(self.url, json={"model": self.model, "messages": messages}, headers=self.headers).json()
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
