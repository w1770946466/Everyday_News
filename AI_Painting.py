import base64
import uuid
import json
import hashlib
import urllib.parse
import requests



QQ_MODE = "CHINA"
with open(r'./OIP.jpg','rb') as f:
    img_buffer = f.read()


# img_buffer =Image.open(r'C:\Users\木倾\Desktop\NewPro\V2raytoClash\OIP.jpg').tobytes()


def qq_request(img_buffer):
    v4uuid = str(uuid.uuid4())
    images = base64.b64encode(img_buffer).decode()

    data_report = {
        'parent_trace_id': '4c689320-71ba-1909-ab57-13c0804d4cc6',
        'root_channel': '',
        'level': 0
    }

    obj = {
        'busiId': 'different_dimension_me_img_entry',#'ai_painting_anime_entry',
        'images': [
            images,
        ],
        'extra': json.dumps({
            'face_rects': [],
            'version': 2,
            'platform': 'web',
            'data_report': data_report
        })
    }
    #print(images)
    sign = signV1(obj)
    #url = "https://ai.tu.qq.com/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process"
    url = "https://ai.tu.qq.com/overseas/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process"
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://h5.tu.qq.com',
        'Referer': 'https://h5.tu.qq.com/web/ai-2d/cartoon/index?jump_qq_for_play=true',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-sign-value': sign,
        'x-sign-version': 'v1'
    }

    timeout = 30000
    # print(type(obj))
    print(sign)
    # print(obh)
    proxies = {
        "http":"http://27.42.168.46:55481",
    }
    response = requests.post(url, json = obj, headers = headers, proxies=proxies, timeout = timeout)
    data = response.json() or {}
    print(data)
    print(type(obj))
    #return json.loads(data)



def signV1(obj):
    s = json.dumps(obj)
    #print(str(len(s)).encode())
    return hashlib.md5(
        b'https://h5.tu.qq.com' + str(len(s)).encode() + b'HQ31X02e'
    ).hexdigest()

qq_request(img_buffer)
