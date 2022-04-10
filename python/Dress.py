import requests
from requests import post
import parsel
import os

url = "http://www.weather.com.cn/weather1d/101120111.shtml#input"
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
html = requests.get(url,headers= header)
html.encoding = html.apparent_encoding
#print(html.text)
selector = parsel.Selector(html.text)
#print(selector)
live = selector.css('.livezs .clearfix li em::text').getall()#生活指数
#print(live)
live_state = selector.css('.livezs .clearfix li span::text').getall()#生活指数优劣
#print(live_state)
live_des = selector.css('.livezs .clearfix li p::text').getall()#生活指数建议
#print(live_des)

live_tem = selector.css('.tem span::text').getall()#最高最底气温
#print(live_tem)

live_time = selector.css('h1 i::text').get()#更新时间

#print(live_time)

time = "🌏" + "今日更新时间："+ live_time + "\n\n"
tem = "🌞" + "今日最高气温："+ live_tem[0] + "℃" + "\n" + "🌤今日最低气温：" + live_tem[1] + "℃" + "\n\n"
cold = "🤧" + live[0] + ":" + live_state[0] + "\n" + live_des[0] + "\n\n"
sport = "🏃" + live[1] + ":" + live_state[1] + "\n" + live_des[1] + "\n\n"
allergy = "😖" + live[2] + ":" + live_state[2] + "\n" + live_des[2] + "\n\n"
dress = "👕" + live[3] + ":" + live_state[3] + "\n" + live_des[3] + "\n\n"
wash_car = "🚗" + live[4] + ":" + live_state[4] + "\n" + live_des[4] + "\n\n"
Ultraviolet = "😎" + live[5] + ":" + live_state[5] + "\n" + live_des[5]


TOKEN = os.environ.get("TOKEN")	#获取TG机器人的TOKEN
CHAT_ID = os.environ.get("CHAT_ID")	#获取推送消息的CHAT_ID

telegram_message = time+tem+cold+sport+allergy+dress+wash_car+Ultraviolet	#需要推送的信息

print(telegram_message)

params = (
    ('chat_id', CHAT_ID),
    ('text', telegram_message),
    ('parse_mode', "Markdown"), #可选Html或Markdown
    ('disable_web_page_preview', "yes")
)


telegram_url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
telegram_req = post(telegram_url, params=params)
print(telegram_req)
