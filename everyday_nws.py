import json
import locale
from time import time, localtime, strftime
import cn2an as cn2an
import cv2
import numpy as np
import requests
from PIL import ImageFont, Image, ImageDraw
from requests import post
import matplotlib.font_manager as fm

# 天行数据的key
tx_key = '7a451b8515e509232c9bf25a62ef6583'


def img():
    # 加载背景图片
    bk_img = cv2.imread("base.jpg")
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
    draw.text((100,28), news(), font=font_small, fill=(255, 255, 255))
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
    req_url = 'http://api.tianapi.com/networkhot/index?key=' + tx_key
    response = requests.get(req_url)
    loads = json.loads(response.text)
    news_list = loads.get('newslist')
    news = ''
    for index in range(len(news_list)):
        if index > 14:
            return news
        title = news_list[index].get('title')
        if len(title) > 25:
            title = title[:25] + '\n   ' + title[25:]
        news += str(index + 1) + '、' + title + '\n\n'
    return news


# 名言
def verse():
    req_url = 'http://api.tianapi.com/mingyan/index?key=' + tx_key
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
    return strftime("%Y年%m月%d日", localtime(time()))


# 精美局子
def sentence():
    req_url = 'http://api.tianapi.com/dujitang/index?key=' + tx_key
    response = requests.get(req_url)
    loads = json.loads(response.text)
    verse_list = loads.get('newslist')
    content = verse_list[0].get('content')
    if len(content) > 18:
        content = content[:18] + '\n' + content[18:36] + '\n' + content[36:]
    return content

#推送TG图片
def post_tg():
    TOKEN = "1914492138:AAENFE40dRpcq5tGtNOOdB1vyURoohHCbxQ"
    CHAT_ID = "1116181878"


    request_url = "https://api.telegram.org/bot" + TOKEN + "/sendMediaGroup"
    params = {
        "chat_id": CHAT_ID
        , "media":
        """[
            {
                "type": "photo"
                , "media": "attach://random-name-1"}, 
            {
                "type": "photo"
                , "media": "attach://random-name-2"}
        ]"""
    }

    files = {
        "random-name-1": open(r"news.jpg", "rb")
        , "random-name-2": open(r"base.jpg", "rb")
    }

    result = requests.post(request_url, params= params, files= files)
    if str(result) =="<Response [200]>":
        print("图片传输完成请注意查收！")
    else:
        print("err!")


if __name__ == '__main__':
    img()
    print("*****图片制作完成*****"+"\n"+"*****正在传输...*****")
    post_tg()
    
