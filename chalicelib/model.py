import json
import time
from botocore.exceptions import ClientError
import logging


class Image(object):
    def __init__(self, msg_id, img_id, img, width, height, timestamp):
        self.msg_id = msg_id
        self.img_id = img_id
        self.img = img
        self.width = int(width)
        self.height = int(height)
        self.timestamp = timestamp

    def __str__(self):
        return '[IMAGE] msg_id: {}, img_id: {}, time: {}, width: {}, height: {}'.format(
            self.msg_id, self.img_id, self.timestamp, self.width, self.height
        )

    def to_dict(self):
        d = {key: val for key, val in self.__dict__.items()}
        d['Schema'] = 'Image'
        return d

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d):
        return cls(d['msg_id'], d['img_id'], d['img'], d['width'], d['height'], d['timestamp'])

    @classmethod
    def from_json(cls, s):
        d = json.loads(s)
        return cls.from_dict(d)

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        return self.msg_id == other.msg_id and \
               self.img == other.img and self.width == other.width and \
               self.height == other.height and self.img_id == self.img_id

    def put_by_id(self, s3, bucket, key=None):
        try:
            s3.put_object(
                Bucket=bucket,
                Key=key if key is not None else self.img_id,
                Body=self.to_json()
            )
            msg = Message(self.msg_id, self.img_id, 'success', str(time.time()))
        except ClientError as e:
            msg = Error(self.msg_id, self.img_id, e.response['Error']['Code'], str(time.time()))
            logging.error(msg)
        return msg

    @classmethod
    def get_by_id(cls, s3, bucket, msg_id, img_id):
        try:
            obj = s3.get_object(
                Bucket=bucket,
                Key=img_id,
            )
            ss = obj['Body'].read().decode('utf-8')
            js = json.loads(ss)
            obj = cls.from_dict(js)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logging.error(e)
                obj = Error(msg_id, img_id, 'NoSuchKey', time.time())
            else:
                raise e
        return obj


class Message(object):
    def __init__(self, msg_id, img_id, msg, timestamp):
        self.msg_id = msg_id
        self.img_id = img_id
        self.msg = msg
        self.timestamp = timestamp

    def __str__(self):
        return '[MESSAGE] msg_id: {}, img_id: {}, time: {}, msg: {}'.format(
            self.msg_id, self.img_id, self.timestamp, self.msg
        )

    def to_dict(self):
        d = {key: val for key, val in self.__dict__.items()}
        d['Schema'] = 'Message'
        return d

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d):
        return cls(d['msg_id'], d['img_id'], d['msg'], d['timestamp'])

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.msg_id == other.msg_id and self.img_id == other.img_id and self.msg == other.msg

    @classmethod
    def build_success_message(cls, msg_id, img_id):
        return cls(msg_id, img_id, 'success', time.time())


class Error(object):
    def __init__(self, msg_id, img_id, msg, timestamp):
        self.img_id = img_id
        self.msg = msg
        self.msg_id = msg_id
        self.timestamp = timestamp

    def __str__(self):
        return '[ERROR] msg_id: {}, img_id:{}, msg: {}, time: {}'.format(
            self.msg_id, self.img_id, self.msg, self.timestamp
        )

    def to_dict(self):
        d = {key: val for key, val in self.__dict__.items()}
        d['Schema'] = 'Error'
        return d

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d):
        return cls(d['msg_id'], d['img_id'], d['msg'], d['timestamp'])

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.msg_id == other.msg_id and self.img_id == other.img_id and self.msg == other.msg


class HayMsg(object):
    def __init__(self):
        self.messages = []

    def add_msg(self, msg):
        self.messages.append(msg)

    def add_msgs(self, msgs):
        self.messages.extend(msgs)

    def __str__(self):
        return '\n'.join(['[HayMSG]: '] + ['  ' + str(i) for i in self.messages])

    def to_dict(self):
        return {'messages': [msg.to_dict() for msg in self.messages]}

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def construct_obj(d):
        if d['Schema'] == 'Message':
            return Message.from_dict(d)
        elif d['Schema'] == 'Error':
            return Error.from_dict(d)
        elif d['Schema'] == 'Image':
            return Image.from_dict(d)
        else:
            raise NotImplementedError('Not support this type.')

    @classmethod
    def from_dict(cls, d):
        obj = cls()
        for col in d['messages']:
            obj.messages.append(cls.construct_obj(col))
        return obj

    @classmethod
    def from_json(cls, j):
        d = json.loads(j)
        return cls.from_dict(d)

    def __len__(self):
        return len(self.messages)

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        if len(self.messages) != len(other):
            return False

        for a, b in zip(self.messages, other.messages):
            if a != b:
                return False
        return True

    def __getitem__(self, item):
        return self.messages[item]
