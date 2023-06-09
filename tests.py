import unittest


class ChatBotTestCase(unittest.TestCase):
    def test_azure_gpt_3(self):
        from chatbot import from_bot_map_config
        from util import load_config
        config = load_config('config.json')
        bot_map = from_bot_map_config(config['bot_map'])
        print(bot_map['gpt-3'].chat('测试'))
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
