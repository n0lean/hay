from chalicelib.model import Image, HayMsg
import base64
import time
import requests


def send_img(path):
    with open(path, 'rb') as f:
        b64_f = base64.b64encode(f.read()).decode('ascii')
    haymsg = HayMsg()
    img = Image('test_msg', 'imagetest', b64_f, 10, 10, str(time.time()))
    haymsg.add_msg(img)
    print(haymsg.to_json())
    # r = requests.post('https://79dcwe44n1.execute-api.us-east-1.amazonaws.com/api/img',
    #                   data=haymsg.to_json())
    # print(r.json())


if __name__ == '__main__':
    send_img('../test/test_img.jpg')
