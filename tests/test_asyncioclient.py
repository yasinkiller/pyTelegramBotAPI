from unittest import TestCase

import asyncio

from TelegramBotAPI.client.asyncioclient import AsyncioClient
from TelegramBotAPI.types.methods import getUpdates, sendMessage, sendPhoto

import env


def aioloop(func):
    def _inner_(*args, **kwargs):
        c = asyncio.coroutine(func)
        f = c(*args, **kwargs)
        l = asyncio.get_event_loop()
        l.run_until_complete(f)
    return _inner_


class TestAsyncioClient(TestCase):
    _client = None

    def setUp(self):
        if self._client is None:
            self._client = AsyncioClient(env.token, self._on_update, env.proxy)

    def _on_update(self, message):
        pass

    @aioloop
    def test_poll(self):
        m = getUpdates()
        m.timeout = 5
        m.limit = 5
        updates = yield from self._client.send_method(m)

        for update in updates:
            print(update)

    @aioloop
    def test_send(self):
        m = sendMessage()
        m.chat_id = env.uid
        m.text = "Hi there"
        resp = yield from self._client.send_method(m)
        print(resp)

    @aioloop
    def test_send_photo(self):
        m = sendPhoto()
        m.chat_id = env.uid
        m.caption = "What is this?"
        import os
        m.photo = os.path.join(os.path.split(__file__)[0], "test.jpg")

        resp = yield from self._client.send_method(m)
        print(resp)

