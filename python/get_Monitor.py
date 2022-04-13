import requests
import parsel
import json
import os
import execjs
from requests import post

#获取新闻
def get_news():
    url = "https://www.csmonitor.com/"
    response = requests.get(url)
    selector = parsel.Selector(response.text)
    title = selector.css("h3 span::text").get()#最大新闻标题
    url = selector.css(".ezc-csm-story-link::attr(href)").get()#新闻地址

    re_ul = "https://www.csmonitor.com"+url
    re = requests.get(re_ul)
    selector2 = parsel.Selector(re.text)
    txt = selector2.css(".eza-caption::text").get()#新闻文章简介
    times = selector2.css("#date-published::text").get()#新闻时间
    #print(times)
    return txt,title,times

#百度翻译所需数据
def get_sign(query):
    baidu_js = '''
        var i = '320305.131321201'

        function n(r, o) {
            for (var t = 0; t < o.length - 2; t += 3) {
                var a = o.charAt(t + 2);
                a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a), a = "+" === o.charAt(t + 1) ? r >>> a : r << a, r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
            }
            return r
        }

        function e(r) {
            var o = r.match(/[\\uD800-\\uDBFF][\\uDC00-\\uDFFF]/g);
            if (null === o) {
                var t = r.length;
                t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
            } else {
                for (var e = r.split(/[\\uD800-\\uDBFF][\\uDC00-\\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++) "" !== e[C] && f.push.apply(f, a(e[C].split(""))), C !== h - 1 && f.push(o[C]);
                var g = f.length;
                g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
            }
            var u = void 0, l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
            u = null !== i ? i : (i = window[l] || "") || "";
            for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
                var A = r.charCodeAt(v);
                128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)), S[c++] = A >> 18 | 240, S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224, S[c++] = A >> 6 & 63 | 128), S[c++] = 63 & A | 128)
            }
            for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++) p += S[b], p = n(p, F);
            return p = n(p, D), p ^= s, 0 > p && (p = (2147483647 & p) + 2147483648), p %= 1e6, p.toString() + "." + (p ^ m)
        }

        // console.log(e('测试'))
        '''
    sign = execjs.compile(baidu_js).call('e', query)
    return sign

#百度翻译
def baidu_translator(txt,sign):
    cookies = {
        'BIDUPSID': '57BC447DE24733422B059674A5B35CAB',
        'PSTM': '1619457093',
        'BAIDUID': '57BC447DE247334206A4C852F901F285:FG=1',
        '__yjs_duid': '1_72d5e43db3f651c78c6f7c56ccb3a8351619585763307',
        'Hm_lvt_64ecd82404c51e03dc91cb9e8c025574': '1620131390',
        'REALTIME_TRANS_SWITCH': '1',
        'HISTORY_SWITCH': '1',
        'FANYI_WORD_SWITCH': '1',
        'SOUND_SPD_SWITCH': '1',
        'SOUND_PREFER_SWITCH': '1',
        'H_WISE_SIDS': '110085_127969_177371_178384_178529_178619_179347_179379_179460_179620_181136_181398_181588_181709_182000_182243_182273_182530_182860_183030_183327_183582_183611_183928_183976_184012_184267_184320_184440_184560_184794_184809_184894_185029_185037_185268_185517_185651_185879_186039_186314_186317_186412_186580_186597_186635_186644_186662_186664_186677_186833_186840_186844_186877_187061_187088_187181_187187_187202_187215_187287_187327_187390_187432_187448_187533_187670_187828_187929_188118_188131_188297_188427_8000089_8000120_8000137_8000143_8000146_8000149_8000163_8000166_8000175_8000186',
        'MAWEBCUID': 'web_WjnznTKeINwjAOKHXBByfyCMgOtREJoKEOTgnnGCIlcmPKLtQH',
        'APPGUIDE_10_0_2': '1',
        'BAIDUID_BFESS': '57BC447DE247334206A4C852F901F285:FG=1',
        'RT': r'z=1&dm=baidu.com&si=ljl03aywmvo&ss=l0gbvtrc&sl=d&tt=10kt&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=iiid&ul=ijzz&hd=ik1j',
        'BDORZ': 'FFFB88E999055A3F8A630C64834BD6D0',
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://fanyi.baidu.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://fanyi.baidu.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,es-AR;q=0.8,es;q=0.7,en;q=0.6',
        'dnt': '1',
        'sec-gpc': '1',
    }

    params = (
        ('from', 'en'),
        ('to', 'zh'),
    )

    data = {
      'from': 'en',
      'to': 'zh',
      'query': txt,
      'transtype': 'realtime',
      'simple_means_flag': '3',
      'sign': sign,
      'token': '9b33a043d23049f8b52092f06ad06d87',
      'domain': 'common'
    }

    response = requests.post('https://fanyi.baidu.com/v2transapi', headers=headers, params=params, cookies=cookies, data=data)
    if response.status_code == 200:
        result = json.loads(response.text)
        #print(result)
        traslation = result['trans_result']['data'][0]['dst']
        word = result['trans_result']['keywords']
        im = ''
        for i in word:
        	for value in i.values():
        		if isinstance(value,list):
        			im += value[0] + "    "
        		else:
        			im += value + "    "
        im = im.split("    ")
        im.pop(-1)
        zhongdian = ''
        for i in range(0,len(im),2):
            zhongdian += im[i+1] + '：' + im[i] + "\n"
        return traslation,zhongdian
    else:
        print("百度词典调用失败")
        return None
#TG
def post_tg(message):
    telegram_message = f"{message}"
    chat_id = os.environ.get("CHAT_ID")
    tg_token = os.environ.get("TOKEN")
    params = (
        ('chat_id', chat_id),
        ('text', telegram_message),
        ('parse_mode', "Markdown"), #可选Html或Markdown
        ('disable_web_page_preview', "yes")
    )    
    telegram_url = "https://api.telegram.org/bot" + tg_token + "/sendMessage"
    telegram_req = post(telegram_url, params=params)
    telegram_status = telegram_req.status_code
    if telegram_status == 200:
        print(f"INFO: Telegram Message sent")
    else:
        print("Telegram Error")

#执行翻译获取消息
def main(word):
    sign = get_sign(word)
    mean = baidu_translator(word,sign)[0]#翻译句子
    im = baidu_translator(word,sign)[1]#重点单词
    return mean,im

if __name__ == '__main__':
    txt  = get_news()[0]#获取的英文内容
    title  = get_news()[1]#获取的文章标题
    times = get_news()[2]#获取的更新时间
    #print(txt)
    biaoti = main(title)[0]#标题的翻译
    juzi = main(txt)[0]#英语句子的翻译
    yisi = main(txt)[1]#重点单词
    message = "🎉基督教科学箴报\n\n"+"🎊更新时间："+times+"\n"+"🎈"+title+"\n"+biaoti+"\n\n"+"🎀"+txt+"\n"+juzi+"\n\n"+"📚重点单词积累：\n"+yisi
    print(message)
    post_tg(message)
    #print("发送完成！！")"""
