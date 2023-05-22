import os
from functools import partial
from json import dumps
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

from chatbot import from_bot_map_config
from util import load_config, logger

dumps = partial(dumps, ensure_ascii=False, separators=(',', ':'))

app = FastAPI()
app.add_middleware(CORSMiddleware)

config = load_config(os.environ['CONFIG_FILE'])
bot_map = from_bot_map_config(config['bot_map'])
token_list: list = config['token_list']


@app.post('/api/chat/{bot}')
async def chat_api(bot: str, body: dict, token: Annotated[str | None, Header()]):
    assert token in token_list
    logger.debug(dumps(body))
    json_response = bot_map[bot].process(body)
    logger.debug(dumps(json_response))
    return {}


def main():
    uvicorn.run(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
