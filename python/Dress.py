import requests
from requests import post
import parsel
import os
import json

url = "http://www.weather.com.cn/weather1d/101120111.shtml"
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,es-AR;q=0.8,es;q=0.7,en;q=0.6",
    "Cache-Control": "no-cache",
    "Cookie": "f_city=%E4%B8%B4%E6%B2%82%7C101120901%7C; userNewsPort0=1",
    "dnt": "1",
    "Host": "www.weather.com.cn",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "sec-gpc": "1",
    "Upgrade-Insecure-Requests": "1"
}

html = requests.get(url,headers= header)
html.encoding = html.apparent_encoding
selector = parsel.Selector(html.text)
#print(selector)
temp = selector.css('script::text').getall()[1]
#将字符串转字典
temp = temp.replace("var observe24h_data = ",'')
temp = temp.replace(";", '')
js = json.loads(temp)#字符串转json
#print(js['od']["od2"])
lose_tem = []
most_tem = []
for i in js['od']["od2"]:
    lose_tem.append(i["od21"])
    most_tem.append(i["od22"])
    #print("最低温度"+i["od21"]+"  /最高温"+i["od22"])
# print(lose_tem,"\n",most_tem)
print(max(lose_tem),max(most_tem))

live = selector.css('.livezs .clearfix li em::text').getall()#生活指数
#print(live)
live_state = selector.css('.livezs .clearfix li span::text').getall()#生活指数优劣
#print(live_state)
live_des = selector.css('.livezs .clearfix li p::text').getall()#生活指数建议
#print(live_des)

live_time = selector.css('h1 i::text').get()#更新时间

#print(live_time)

time = "🌏" + "今日更新时间："+ live_time + "\n\n"
tem = "🌞" + "今日最高气温："+ max(most_tem) + "℃" + "\n" + "🌤今日最低气温：" + max(lose_tem) + "℃" + "\n\n"
cold = "🤧" + live[0] + ":" + live_state[0] + "\n" + live_des[0] + "\n\n"
sport = "🏃" + live[1] + ":" + live_state[1] + "\n" + live_des[1] + "\n\n"
allergy = "😖" + live[2] + ":" + live_state[2] + "\n" + live_des[2] + "\n\n"
dress = "👕" + live[3] + ":" + live_state[3] + "\n" + live_des[3] + "\n\n"
wash_car = "🚗" + live[4] + ":" + live_state[4] + "\n" + live_des[4] + "\n\n"
Ultraviolet = "😎" + live[5] + ":" + live_state[5] + "\n" + live_des[5]
print(tem)

TOKEN = os.environ.get("TOKEN")	#获取TG机器人的TOKEN
CHAT_ID = os.environ.get("CHAT_ID")	#获取推送消息的CHAT_ID

telegram_message = time+tem+cold+sport+allergy+dress+wash_car+Ultraviolet	#需要推送的信息

params = (
    ('chat_id', CHAT_ID),
    ('text', telegram_message),
    ('parse_mode', "Markdown"), #可选Html或Markdown
    ('disable_web_page_preview', "yes")
)

try:
	telegram_url = "https://api.telegram.org/bot" + TG_TOKEN + "/sendMessage"
	telegram_req = post(telegram_url, params=params)
	print("推送送成功！！")
except:
	print("推送失败请检查！！")
