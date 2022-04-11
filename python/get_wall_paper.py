import requests
import parsel
import os

url = "https://wallhaven.cc/search?categories=110&purity=100&resolutions=1920x1080&sorting=hot&order=desc"#1920x1080是图片比率
response = requests.get(url)
selector = parsel.Selector(response.text)
url = selector.css('.preview::attr(href)').getall()
for i in url:
	re = requests.get(i)
	selector2 = parsel.Selector(re.text)
	url2 = selector2.css('#wallpaper::attr(src)').getall()
	title = selector2.css('title::text').get()
	title = title.split(',')
	for u in url2:
		print(u)
		r = requests.get(u)
		with open(r"./1920x1080/"+title[0]+".jpg","wb") as f:
			f.write(r.content)
			f.close()
print("下载完成")
