import unittest
from chalicelib.model import *
import time
import json


class TestModel(unittest.TestCase):
    def test_msg(self):
        messages = HayMsg()
        msg = Message('123', 'hello world!', str(time.time()))
        messages.add_msg(msg)

        json_msgs = messages.to_json_str()
        d = json.loads(json_msgs)

        new_messages = HayMsg.from_json(d)

        print(new_messages)
        print(messages)
        assert new_messages == messages

    def test_img(self):
        imgs = HayImg()
        img = Image('123', '123', 12, 21, '123')
        imgs.add_image(img)

        json_imgs = imgs.to_json_str()
        d = json.loads(json_imgs)

        new_imgs = HayImg.from_json(d)

        print(imgs)
        print(new_imgs)
        assert new_imgs == imgs
