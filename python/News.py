import requests
import random
import os
import json
from datetime import *

# 每日简报
def news(TX_KEY):
    req_url = 'http://api.tianapi.com/networkhot/index?key=' + TX_KEY
    response = requests.get(req_url)
    loads = json.loads(response.text)
    news_list = loads.get('newslist')
    new = '<p>'
    for index in range(len(news_list)):
        if index > 12:
            title = news_list[index].get('title')
            if len(title) > 25:
                title = title[:25] + '<br>' + title[25:]
            new += str(index + 1) + '、' + title + '<br>'
        title = news_list[index].get('title')
    new += '</p>'
    return new

# 名言
def verse(TX_KEY):
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
def sentence(TX_KEY):
    req_url = 'http://api.tianapi.com/dujitang/index?key=' + TX_KEY
    response = requests.get(req_url)
    loads = json.loads(response.text)
    verse_list = loads.get('newslist')
    content = verse_list[0].get('content')
    if len(content) > 18:
        content = content[:18] + '\n' + content[18:36] + '\n' + content[36:]
    return content

  #TG发消息
def post_tg(message):
    telegram_message = f"{message}"
    chat_id = os.environ.get("CHAT_ID")
    tg_token = os.environ.get("TOKEN")
    params = (
        ('chat_id', chat_id),
        ('text', telegram_message),
        ('parse_mode', "Html"), #可选Html或Markdown
        ('disable_web_page_preview', "yes")
    )    
    telegram_url = "https://api.telegram.org/bot" + tg_token + "/sendMessage"
    telegram_req = requests.post(telegram_url, params=params)
    telegram_status = telegram_req.status_code
    if telegram_status == 200:
        print(f"INFO: Telegram Message sent")
    else:
        print("Telegram Error",telegram_req.text)

if __name__ == '__main__':
    TX_KEY = os.environ.get("TX_KEY")
    message = news(TX_KEY)
    post_tg(message)
  
