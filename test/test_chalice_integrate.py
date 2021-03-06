from unittest import TestCase
from chalice.config import Config
from chalice import local
from chalicelib import model
from app import app
from moto import mock_s3
import boto3
import json
import base64
import time


BUCKET = 'anda-bucket-cloudphoto-app'


class TestApp(TestCase):
    def setUp(self):
        self.mock = mock_s3()
        self.mock.start()
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=BUCKET)
        self.lg = local.LocalGateway(app, Config())

    def tearDown(self):
        self.mock.stop()

    # def test_get_image(self):
    #     new_img = model.Image(
    #         msg_id='1234', img_id='12345', img='asdfasdfasdf', width=10, height=20, timestamp='123123'
    #     )
    #     s3 = boto3.client('s3', region_name='us-east-1')
    #     new_img.put_by_id(s3, BUCKET)
    #     test_hay = model.HayMsg()
    #     test_hay.add_msg(new_img)
    #
    #     response = self.lg.handle_request(
    #         method='GET',
    #         path='/img/12345',
    #         headers={},
    #         body=''
    #     )
    #     new_hay = model.HayMsg.from_json(response['body'])
    #     self.assertEqual(new_hay, test_hay)
    #
    # def test_get_non_exist(self):
    #     response = self.lg.handle_request(
    #         method='GET',
    #         path='/img/123',
    #         headers={},
    #         body=''
    #     )
    #     new_hay = model.HayMsg.from_json(response['body'])
    #
    #     err = model.Error(
    #         new_hay[0].msg_id, new_hay[0].img_id,
    #         'NoSuchKey', '123'
    #     )
    #     res_hay = model.HayMsg()
    #     res_hay.add_msg(err)
    #     self.assertEqual(res_hay, new_hay)
    #
    # def test_put_image(self):
    #     new_img = model.Image(
    #         msg_id='1234', img_id='12345', img='asdfasdfasdf', width=10, height=20, timestamp='123123'
    #     )
    #     test_hay = model.HayMsg()
    #     test_hay.add_msg(new_img)
    #
    #     response = self.lg.handle_request(
    #         method='POST',
    #         path='/img',
    #         headers={},
    #         body=test_hay.to_json()
    #     )
    #
    #     res_hay = model.HayMsg.from_json(response['body'])
    #
    #     s3 = boto3.client('s3', region_name='us-east-1')
    #     target = model.Image.get_by_id(s3, BUCKET, '1234', res_hay[0].img_id)
    #     tar_hay = model.HayMsg()
    #     tar_hay.add_msg(target)
    #     self.assertEqual(response['statusCode'], 200)
    #     self.assertEqual(tar_hay, test_hay)

    # def test_hello(self):
    #     response = self.lg.handle_request(
    #         method='GET',
    #         path='/hello',
    #         headers={},
    #         body=''
    #     )
    #     message = model.Message('123', '123', 'hello world!', '123')
    #     mock = model.HayMsg()
    #     mock.add_msg(message)
    #     res = model.HayMsg.from_json(response['body'])
    #     self.assertEqual(response['statusCode'], 200)
    #     self.assertEqual(res, mock)
    #
    # def test_combo(self):
    #     # pre save
    #     s3 = boto3.client('s3', region_name='us-east-1')
    #     pre_img = model.Image(
    #         msg_id='1234', img_id='12345', img='asdfasdfasdf', width=10, height=20, timestamp='123123'
    #     )
    #     pre_msg = pre_img.put_by_id(s3, BUCKET)
    #
    #     test_hay = model.HayMsg()
    #     new_img = model.Image(
    #         msg_id='1234', img_id='125', img='asdfasdfasdf', width=10, height=20, timestamp='123123'
    #     )
    #     new_req = model.Message(
    #         msg_id='1234', img_id=pre_msg.img_id, msg='Get image', timestamp='12312314'
    #     )
    #     test_hay.add_msg(new_img)
    #     test_hay.add_msg(new_req)
    #
    #     response = self.lg.handle_request(
    #         method='POST',
    #         path='/img',
    #         headers={},
    #         body=test_hay.to_json()
    #     )
    #
    #     res_hay = model.HayMsg.from_json(response['body'])
    #     self.assertTrue(isinstance(res_hay[0], model.Message))
    #     self.assertTrue(isinstance(res_hay[1], model.Image))
    #
    # def test_local_img(self):
    #     path = './test/test_img.jpg'
    #     with open(path, 'rb') as f:
    #         b64_f = base64.b64encode(f.read()).decode('ascii')
    #     haymsg = model.HayMsg()
    #     img = model.Image('test_msg', 'image_test', b64_f, 10, 10, str(time.time()))
    #     haymsg.add_msg(img)
    #
    #     response = self.lg.handle_request(
    #         method='POST',
    #         path='/img',
    #         headers={},
    #         body=haymsg.to_json()
    #     )
    #
    #     res_hay = model.HayMsg.from_json(response['body'])
    #     print(res_hay.to_json())
    #     self.assertTrue(isinstance(res_hay[0], model.Message))
