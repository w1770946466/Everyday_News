from bs4 import BeautifulSoup
import os
import requests
import json


def get_weibo():
    # 设置 头数据
    headers = {'scheme': 'https',
            'accept': 'text/html, application/xhtml+xml, application/xml',
            'accept-language': 'zh-CN, zh',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
            }
    # get请求 热榜地址
    r = requests.get(
        'https://weibo.com/ajax/statuses/hot_band', headers=headers)
    # 加在请求结果为对象
    data = json.loads(r.text)
    #print(data)
    # 总计内容
    textStr = ''
    # 遍历列表数据
    for index, item in enumerate(data['data']['band_list']):
        if 'topic_ad' not in item:
            # 标题
            note = item['note']
            word = item['word']
            # 热值
            raw_hot = item['num']
            # 链接
            url=''
            if 'mblog' in item:
                url = item['mblog']['text']
                soup = BeautifulSoup(url, 'html.parser')
                if type(soup.find('a')) != NoneType:
                    url=soup.find('a').get('href')
            # 标签
            if 'icon_desc' in item:
                label_name = item['icon_desc']
            else:
                label_name = '无'
            itemStr = '{}、【{}】{}【{}】'.format(index+1, label_name, word, str(raw_hot))
            if index < 21:
                textStr += str(itemStr+'\n')
    #print(textStr)
    return textStr
        
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
        
        
def main():
  weibo = get_weibo()
  post_tg(weibo)
  
  
  
if __name__ == '__main__':
    main()
