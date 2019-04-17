from chalice import Chalice
import time
from chalicelib.model import *
import boto3
from botocore.exceptions import ClientError
from botocore.vendored import requests
from chalice import NotFoundError
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
app = Chalice(app_name='hay')
s3 = boto3.client('s3', region_name='us-west-1')
BUCKET = 'cloudphoto-hay'


def build_success_message(_id, msg_str, timestamp):
    msg = Message(_id, msg_str, timestamp)
    obj = HayMsg()
    obj.add_msg(msg)
    return obj


def build_error_message(code, err):
    response = HayMsg()
    msg = Error(code, err)
    response.add_msg(msg)
    return response


@app.route('/hello', methods=['GET'])
def hello():
    messages = HayMsg()
    msg = Message('123', 'hello world!', str(time.time()))
    messages.add_msg(msg)
    return messages.to_json_str()


@app.route('/img/{img_id}', methods=['GET'])
def get_image(img_id):
    response = HayImg()
    try:
        obj = s3.get_object(
            Bucket=BUCKET,
            Key=img_id,
        )
        ss = obj['Body'].read().decode('utf-8')
        js = json.loads(ss)
        img = Image.from_json(js)
        response.add_image(img)
    except KeyError as e:
        raise e
    except NotFoundError as e:
        logging.error('NotFoundError' + str(e))
        response = HayMsg()
        err = Error('-1', 'Exception: ' + str(e))
        response.add_msg(err)
        return response.to_json_str()
    return response.to_json_str()


@app.route('/img', methods=['POST'])
def save_image():
    body = app.current_request.json_body
    hayimg = HayImg.from_json(body)
    response = HayMsg()
    for img in hayimg.images:
        try:
            s3.put_object(
                Bucket=BUCKET,
                Key=img.id,
                Body=img.to_json_str()
            )
            msg = Message(img.id, 'success', str(time.time()))
            response.add_msg(msg)
        except KeyError as e:
            err = Error('-1', 'Exception: ' + str(e))
            response.add_msg(err)
    return response.to_json_str()
