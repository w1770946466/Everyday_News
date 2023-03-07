#-*- coding: UTF-8 -*-
import json
import re
import time
import requests

i = 0
url = 'https://raw.githubusercontent.com/mondayfirst/XXQG_TiKu/main/%E9%A2%98%E5%BA%93_%E6%8E%92%E5%BA%8F%E7%89%88.json'
response = requests.get(url)
if response.status_code == 200:
    fp = response.content.decode('utf-8')
    print("获取题库成功")
else:
   print("获取题库失败！！")

json_data = json.loads(fp)
for key, value in json_data.items():
    cy = key.replace("        。|", "")
    cy_bc = cy.replace("        。", "")
    cy_k = cy_bc.replace(" ", "")
    cy2 = cy_k.replace("|", "，")
    pie = re.split(r"[\|]", key)
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
    opt = list(pie[0])
    topic = pie[0].replace(" ", "")
    if "".join(opt[0]+opt[1]+opt[2]+opt[3]) == '选择词语':
        if len(pie) == 3:
            strt = options + " " + cy2 + "。" + " " + pie[1] + "	" + pie[2]
        elif len(pie) == 4:
            strt = options + " " + cy2 + "。" + " " + \
                pie[1] + "	" + pie[2] + "	" + pie[3]
        elif len(pie) == 5:
            strt = options + " " + cy2 + "。" + " " + \
                pie[1] + "	" + pie[2] + "	" + pie[3] + "	" + pie[4]
        print("发现选择词语类题目，选项添加到题目中！")
    elif "".join(opt[0]+opt[1]+opt[2]+opt[3]) == '选择正确':
        if len(pie) == 3:
            strt = options + " " + cy2 + "。" + " " + pie[1] + "	" + pie[2]
        elif len(pie) == 4:
            strt = options + " " + cy2 + "。" + " " + \
                pie[1] + "	" + pie[2] + "	" + pie[3]
        elif len(pie) == 5:
            strt = options + " " + cy2 + "。" + " " + \
                pie[1] + "	" + pie[2] + "	" + pie[3] + "	" + pie[4]
        print("发现选择词语类题目，选项添加到题目中！")
    else:
        if len(pie) == 3:
            strt = options + " " + topic + " " + pie[1] + "	" + pie[2]
        elif len(pie) == 4:
            strt = options + " " + topic + " " + \
                pie[1] + "	" + pie[2] + "	" + pie[3]
        elif len(pie) == 5:
            strt = options + " " + topic + " " + \
                pie[1] + "	" + pie[2] + "	" + pie[3] + "	" + pie[4]
    f = open('.\question', 'a', encoding='utf8')
    f.write(strt + "\n")
    f.close()
    i = i + 1
    stri = str(i)
    print("已处理" + stri + "条数据")
