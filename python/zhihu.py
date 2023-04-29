import requests
import os
from bs4 import BeautifulSoup

# 爬取知乎热门内容
def get_zhihu_hot():
    url = "https://www.zhihu.com/hot"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
    }
    response = requests.get(url, headers=headers)
    #print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    hot_list = soup.find_all("div", class_="css-1mx3lj4")
    #print(hot_list)
    hot_titles = []
    hot_content = []
    hot_fire = []
    for item in hot_list:
        title = item.find("h1", class_="css-3yucnr").text
        try:
            content = item.find("div", class_="css-1o6sw4j").text
            hot_content.append(content)#内容缺失
        except:
            pass
        fire = item.find("div", class_="css-1iqwfle").text
        hot_titles.append(title)
        hot_fire.append(fire)
    return hot_titles,hot_fire  #,hot_content

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
    message = ''
    for i in range(len(zhihu[0])):
        message += str(zhihu[0][i]) + '【' + str(zhihu[1][i]) + '】'
    post_tg(message)

if __name__ == '__main__':
    main()
    
    
    
    
