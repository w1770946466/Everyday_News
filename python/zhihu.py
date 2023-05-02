import requests
import os
from bs4 import BeautifulSoup

# 爬取知乎热门内容
def get_zhihu_hot():
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10&desktop=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    hot_titles = []
    hot_url = []
    hot_fire = []
    # 获取问题及答案
    for item in data["data"]:
        if "target" in item :
            question = item["target"]["title"]
            answer = item["target"]["excerpt"]
            url = 'https://www.zhihu.com/question/' + str(item["target"]["id"])
            hot = item["detail_text"]
            hot_titles.append(question)
            hot_url.append(url)
            hot_fire.append(hot)
    return hot_titles,hot_fire,hot_url

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

#运行
def main():
    zhihu = get_zhihu_hot()
    #print(zhihu[0],zhihu[1])
    message = '知乎热榜\n\n'
    for i in range(len(zhihu[0])):
        if i < 20:
            message += str(i+1) + '、' + str(zhihu[0][i]) + '\n【🔥' + str(zhihu[1][i]) + '】\n' + str(zhihu[2][i]) + '\n\n'
    try:
        post_tg(message,message)
    except Eexception as e:
        print(e)
    
    
if __name__ == '__main__':
    main()
    
    
    
    
