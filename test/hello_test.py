import unittest
from chalicelib.model import *
import time


class TestHello(unittest.TestCase):
    def test_hello(self):
        messages = HayMsg()
        msg = Message('123', 'hello world!', str(time.time()))
        messages.add_msg(msg)
        print(messages.to_json_str())
        print(msg.to_json_str())

        imgs = HayImg()
        img = Image('123', b'aaaa', '12', '23', '123')
        imgs.add_image(img)

        print(img.to_json_str())
        print(imgs.to_json_str())
