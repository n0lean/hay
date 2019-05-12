import base64
import time
import requests


def send_img(path):
    with open(path, 'rb') as f:
        b64_f = base64.b64encode(f.read()).decode('ascii')
    print(b64_f)


if __name__ == '__main__':
    send_img('../test/test_img2.jpg')
