import json
import locale
from time import time, localtime, strftime
import cn2an as cn2an
import cv2
import numpy as np
import requests
from PIL import ImageFont, Image, ImageDraw
from requests import post
import random
import os
from datetime import *

def img():
    # 加载背景图片
    bk_img = cv2.imread(base_jpg)
    # 设置需要显示的字体
    #fontpath = fm.findfont(fm.FontProperties())
    fontpath = r'/usr/share/fonts/custom/BOBOHEI-2.otf'
    #print(fontpath)
    font = ImageFont.truetype(fontpath,80)
    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)
    # 绘制文字信息
    today = int(strftime("%w"))
    if 0 == today:
        today = '星期日'
    else:
        today = '星期' + cn2an.an2cn(today)
    # 自行调整此处文字所在位置
    #星期位置
    draw.text((1650, 55), today, font=font, fill=(255, 255, 0))  
    font_small = ImageFont.truetype(fontpath, 35)
    font_sentence = ImageFont.truetype(fontpath, 16)
    #日期位置
    draw.text((900, 55), todayYear(), font=font, fill=(255, 255, 0))
    #新闻位置
    if news()[1] == None:
        draw.text((100,20), news()[0], font=font_small, fill=(255, 255, 255))
    else:
        draw.text((100,20), news()[0], font=font_small, fill=(255, 255, 255))
        draw.text((900,500), news()[1], font=font_small, fill=(255, 255, 255))
    font_red = ImageFont.truetype(fontpath, 40)
    #名句位置
    draw.text((900, 200), verse(), font=font_red, fill=(255, 255, 0))
    bk_img = np.array(img_pil)
    # 展示图片,不需要可注释
    #cv2.imshow("add_text", bk_img)
    cv2.waitKey()
    cv2.imwrite("news.jpg", bk_img)



# 每日简报
def news():
    req_url = 'http://api.tianapi.com/networkhot/index?key=' + TX_KEY
    response = requests.get(req_url)
    loads = json.loads(response.text)
    news_list = loads.get('newslist')
    news = ''
    new = ''
    for index in range(len(news_list)):
        if index > 12:
            title = news_list[index].get('title')
            if len(title) > 25:
                title = title[:25] + '\n   ' + title[25:]
            new += str(index + 1) + '、' + title + '\n\n'
        title = news_list[index].get('title')
        if len(title) > 25:
            title = title[:25] + '\n   ' + title[25:]
        news += str(index + 1) + '、' + title + '\n\n'
    return news,new


# 名言
def verse():
    req_url = 'http://api.tianapi.com/mingyan/index?key=' + TX_KEY
    response = requests.get(req_url)
    loads = json.loads(response.text)
    verse_list = loads.get('newslist')
    source = verse_list[0].get('content')
    saying = verse_list[0].get('author')
    verse_str = '【微语】 ' + source +  "\n\n——" +saying
    resp_verse = verse_str
    if len(verse_str) > 22:
        resp_verse = verse_str[:23] + '\n\n' + verse_str[23:]
    return resp_verse


# 年月日
def todayYear():
    import datetime
    SHA_TZ = timezone(timedelta(hours=8),name='Asia/Shanghai')
    return datetime.datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(SHA_TZ).strftime("%Y年%m月%d日")


# 精美句子
def sentence():
    req_url = 'http://api.tianapi.com/dujitang/index?key=' + TX_KEY
    response = requests.get(req_url)
    loads = json.loads(response.text)
    verse_list = loads.get('newslist')
    content = verse_list[0].get('content')
    if len(content) > 18:
        content = content[:18] + '\n' + content[18:36] + '\n' + content[36:]
    return content

#推送TG图片
def post_tg():
    request_url = "https://api.telegram.org/bot" + TOKEN + "/sendMediaGroup"
    #print(request_url)
    params = {
        "chat_id": CHAT_ID
        , "media":
        """[
            {
                "type": "photo"
                , "media": "attach://random-name-1"}
        ]"""
    }

    files = {
        "random-name-1": open(r"news.jpg", "rb")
    }

    result = requests.post(request_url, params= params, files= files)
    if str(result) =="<Response [200]>":
        print("图片传输完成请注意查收！")
    else:
        print("err!")


if __name__ == '__main__':
    #随机选择底片
    photo_path = './1920x1080'
    files = os.listdir(photo_path)
    base = random.sample(files,1)[0]
    base_jpg = "./1920x1080/" + base
    #天行健key
    global TX_KEY
    TX_KEY = os.environ.get("TX_KEY")
    print(TX_KEY)
    img()
    print("*****图片制作完成*****"+"\n"+"*****正在传输...*****")
    #tg id 和 token
    global TOKEN,CHAT_ID
    CHAT_ID = os.environ.get("CHAT_ID")
    TOKEN = os.environ.get("TOKEN")
    post_tg()
    
