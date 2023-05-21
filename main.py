from flask import Flask, request, jsonify
from chatbot import ChatGPT
import os
import logging
from json import dumps
from functools import partial

dumps = partial(dumps, ensure_ascii=False, separators=(',', ':'))

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger: logging.Logger = logging.getLogger('robot')

api_key: str = os.environ['OPENAI_API_KEY']
model: str = os.environ['OPENAI_MODEL']
bot = ChatGPT(api_key=api_key, model=model)


@app.route('/api/robot/chat', methods=['POST'])
def chat_api():
    body: dict = request.get_json()
    logger.debug(dumps(body))
    json_response = bot.process(body)
    logger.debug(dumps(json_response))

    return jsonify({})


def main():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
