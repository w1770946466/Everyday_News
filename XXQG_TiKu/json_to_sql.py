#-*- coding: UTF-8 -*-
import json
import re
import time
import requests

url = 'https://raw.githubusercontent.com/mondayfirst/XXQG_TiKu/main/%E9%A2%98%E5%BA%93_%E6%8E%92%E5%BA%8F%E7%89%88.json'
response = requests.get(url)
if response.status_code == 200:
    fp = response.content.decode('utf-8')
    print("获取题库成功")
else:
   print("获取题库失败！！")

json_data = json.loads(fp)
for key, value in json_data.items():
    pie = re.split(r"[\|]", key)
#            sort = {'1': }
    if value == pie[1]:
        options = 'A'
    elif value == pie[2]:
        options = 'B'
    elif value == pie[3]:
        options = 'C'
    elif value == pie[4]:
        options = 'D'
    else:
        options = 'NULL'
    str = 'INSERT INTO "tiku" VALUES (' + "'" + key + "'" + ',' + "'" + value + "'" + ", NULL, '" + \
        options + "', '" + \
        time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "');"
# 睿智
#        print(str)
    f = open('.\QuestionBank.db', 'a', encoding='utf8')
    f.write('\n' + str)
    f.close()
