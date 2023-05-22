import os
from functools import partial
from json import dumps

from flask import Flask, request, jsonify

from chatbot import from_bot_map_config
from util import load_config, logger

dumps = partial(dumps, ensure_ascii=False, separators=(',', ':'))

app = Flask(__name__)

config = load_config(os.environ['CONFIG_FILE'])
bot_map = from_bot_map_config(config['bot_map'])
token_list: list = config['token_list']


@app.route('/api/chat/<bot>', methods=['POST'])
def chat_api(bot: str):
    token: str = request.headers['Token']
    assert token in token_list
    body: dict = request.get_json()
    logger.debug(dumps(body))
    json_response = bot_map[bot].process(body)
    logger.debug(dumps(json_response))
    return jsonify({})


def main():
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
