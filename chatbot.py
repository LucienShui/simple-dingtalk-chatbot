from requests.api import post
import os


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
    def __init__(self, api_key: str, endpoint: str = 'https://api.openai-proxy.com',
                 model: str = "gpt-3.5-turbo"):
        self.api_key: str = api_key
        self.url: str = os.path.join(endpoint, '/v1/chat/completions')
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
