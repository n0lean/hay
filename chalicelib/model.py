import json


class Image(object):
    def __init__(self, _id, img, width, height, timestamp):
        self.id = _id
        self.img = img
        self.width = int(width)
        self.height = int(height)
        self.timestamp = timestamp

    def __str__(self):
        return '[IMAGE] id: {}, time: {}, width: {}, height: {}'.format(
            self.id, self.timestamp, self.width, self.height
        )

    def to_json(self):
        return {
            key: val for key, val in self.__dict__.items()
        }

    def to_json_str(self):
        return json.dumps(self.to_json())

    @classmethod
    def from_json(cls, d):
        return cls(d['id'], d['img'], d['width'], d['height'], d['timestamp'])

    @classmethod
    def from_json_str(cls, s):
        d = json.loads(s)
        return cls.from_json(d)

    def __eq__(self, other):
        return self.id == other.id and self.img == other.img and \
               self.width == other.width and self.height == other.height and \
               self.timestamp == other.timestamp


class Message(object):
    def __init__(self, _id, msg, timestamp):
        self.id = _id
        self.msg = msg
        self.timestamp = timestamp

    def __str__(self):
        return '[MESSAGE] id: {}, time: {}, msg: {}'.format(self.id, self.timestamp, self.msg)

    def to_json(self):
        return {
            key: val for key, val in self.__dict__.items()
        }

    def to_json_str(self):
        return json.dumps(self.to_json())

    @classmethod
    def from_json(cls, d):
        return cls(d['id'], d['msg'], d['timestamp'])

    def __eq__(self, other):
        return self.id == other.id and self.msg == other.msg and self.timestamp == other.timestamp


class Error(object):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return '[ERROR] code: {}, msg: {}'.format(self.code, self.msg)

    def to_json(self):
        return {
            key: str(val) for key, val in self.__dict__.items()
        }

    def to_json_str(self):
        return json.dumps(self.to_json())


class HayMsg(object):
    def __init__(self):
        self.messages = []

    def add_msg(self, msg):
        self.messages.append(msg)

    def add_msgs(self, msgs):
        self.messages.extend(msgs)

    def __str__(self):
        return '\n'.join(['[HayMSG]: '] + ['  ' + str(i) for i in self.messages])

    def to_json(self):
        return {'messages': [msg.to_json() for msg in self.messages]}

    def to_json_str(self):
        return json.dumps(self.to_json())

    @classmethod
    def from_json(cls, d):
        obj = cls()
        for col in d['messages']:
            obj.messages.append(Message.from_json(col))
        return obj

    def __len__(self):
        return len(self.messages)

    def __eq__(self, other):
        if len(self.messages) != len(other):
            return False

        for a, b in zip(self.messages, other.messages):
            if a != b:
                return False
        return True


class HayImg(object):
    def __init__(self):
        self.images = []

    def add_image(self, img):
        self.images.append(img)

    def add_images(self, imgs):
        self.images.extend(imgs)

    def __str__(self):
        return '\n'.join(['[HayIMG]: '] + ['  ' + str(i) for i in self.images])

    def to_json(self):
        return {'messages': [msg.to_json() for msg in self.images]}

    def to_json_str(self):
        return json.dumps(self.to_json())

    def __len__(self):
        return len(self.images)

    @classmethod
    def from_json(cls, d):
        obj = cls()
        for col in d['messages']:
            obj.images.append(Image.from_json(col))
        return obj

    def __eq__(self, other):
        if len(self.images) != len(other):
            return False

        for a, b in zip(self.images, other.images):
            if a != b:
                return False
        return True
