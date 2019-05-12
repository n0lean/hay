from moto import mock_s3
import unittest
import boto3
import time
from chalicelib.model import Image, Message, Error
import base64


BUCKET = 'bucket_name'


class S3Test(unittest.TestCase):
    def setUp(self):
        self.mock = mock_s3()
        self.mock.start()

        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=BUCKET)

    def tearDown(self):
        self.mock.stop()

    # def test_image(self):
    #     path = './test/test_img.jpg'
    #     with open(path, 'rb') as f:
    #         b64_f = base64.b64encode(f.read()).decode('ascii')
    #     img = Image('test_msg', 'image_test', b64_f, 10, 10, str(time.time()))
    #
    #     s3 = boto3.client('s3', region_name='us-east-1')
    #     img.put_by_id(s3, BUCKET, None)

        # new_img = Image.get_by_id(s3, BUCKET, img.msg_id, img.img_id)


    # def test_not_found(self):
    #     img = Image('123', '123', 'asdfasdfasdf', 10, 20, time.time())
    #
    #     s3 = boto3.client('s3', region_name='us-east-1')
    #     img.put_by_id(s3, BUCKET, None)
    #
    #     target_id = '12345'
    #     new_img = Image.get_by_id(s3, BUCKET, '123', target_id)
    #     expected = Error('123', target_id, 'NoSuchKey', new_img.timestamp)
    #     assert expected == new_img

