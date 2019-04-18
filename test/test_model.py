import unittest
from chalicelib.model import *
import time
import json


class TestModel(unittest.TestCase):
    def test_msg(self):
        messages = HayMsg()
        msg = Message('123', '123', 'hello world!', str(time.time()))
        messages.add_msg(msg)

        json_msgs = messages.to_json()
        d = json.loads(json_msgs)

        new_messages = HayMsg.from_dict(d)
        assert new_messages == messages

    def test_img(self):
        imgs = HayMsg()
        img = Image('123', '123', '123', 12, 21, '123')
        imgs.add_msg(img)

        json_imgs = imgs.to_json()
        d = json.loads(json_imgs)

        new_imgs = HayMsg.from_dict(d)
        assert new_imgs == imgs
