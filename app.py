from chalice import Chalice
import time
from chalicelib.model import *
import boto3
from botocore.exceptions import ClientError
from botocore.vendored import requests
from chalicelib.utils.aws_util import check_id_available
import logging
import uuid


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
app = Chalice(app_name='hay')

BUCKET = 'anda-bucket-cloudphoto-app'


@app.route('/hello', methods=['GET'])
def hello():
    messages = HayMsg()
    msg = Message(
        msg_id='123', img_id='123', msg='hello world!', timestamp=str(time.time())
    )
    messages.add_msg(msg)
    return messages.to_json()


@app.route('/img/{img_id}', methods=['GET'])
def get_image(img_id):
    s3 = boto3.client('s3', region_name='us-east-1')
    response = HayMsg()
    msg_id = str(uuid.uuid4())
    img = Image.get_by_id(s3, BUCKET, msg_id=msg_id, img_id=img_id)
    response.add_msg(img)
    return response.to_json()


@app.route('/img', methods=['POST'])
def put_image():
    s3 = boto3.client('s3', region_name='us-east-1')
    response = HayMsg()
    body = app.current_request.raw_body.decode()
    hayimg = HayMsg.from_json(body)
    for msg in hayimg.messages:
        if isinstance(msg, Image):
            new_id = str(uuid.uuid4())
            # while not check_id_available(new_id, BUCKET, s3):
            #     new_id = str(uuid.uuid4())
            msg.img_id = new_id

            new_m = msg.put_by_id(s3, BUCKET, new_id)
            response.add_msg(new_m)
        elif isinstance(msg, Message):
            img = Image.get_by_id(s3, BUCKET, msg.msg_id, msg.img_id)
            response.add_msg(img)
        else:
            err = Error(msg.msg_id, msg.img_id, 'Wrong Message', time.time())
            response.add_msg(err)
    return response.to_json()


@app.route('/img', methods=['DELETE'])
def delete_image():
    pass
