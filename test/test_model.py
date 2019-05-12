import unittest
from chalicelib.model import *
import time
import json
import base64


class TestModel(unittest.TestCase):
    def test_msg(self):
        messages = HayMsg()
        msg = Message('123', '123', 'hello world!', str(time.time()))
        messages.add_msg(msg)

        json_msgs = messages.to_json()
        d = json.loads(json_msgs)

        new_messages = HayMsg.from_dict(d)
        assert new_messages == messages
    #
    # def test_img(self):
    #     imgs = HayMsg()
    #     img = Image('123', '123', '123', 12, 21, '123')
    #     imgs.add_msg(img)
    #
    #     json_imgs = imgs.to_json()
    #     d = json.loads(json_imgs)
    #
    #     new_imgs = HayMsg.from_dict(d)
    #     assert new_imgs == imgs
    #
    # def test_local_img(self):
    #     path = './test/test_img.jpg'
    #     with open(path, 'rb') as f:
    #         b64_f = base64.b64encode(f.read()).decode('ascii')
    #     haymsg = HayMsg()
    #     img = Image('test_msg', 'image_test', b64_f, 10, 10, str(time.time()))
    #     haymsg.add_msg(img)
    #     js = haymsg.to_json()
    #     newmsg = HayMsg.from_json(js)
    #
    #     self.assertEqual(newmsg, haymsg)
