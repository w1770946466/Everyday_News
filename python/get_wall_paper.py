import requests
import parsel
import os
import random
import time
from tqdm import tqdm


def main():
	pages = []
	while (len(pages)<2): #随机获取2个不相等的
		page = random.randint(1,12380)
		if page not in pages:
			pages.append(page)
	for i in pages:#拼接获取url地址
		url = "https://wallhaven.cc/search?categories=110&purity=100&atleast=1920x1080&sorting=date_added&order=desc&page={0}".format(i)#1920x1080是图片比率
		print("正在下载第{0}页所有图片".format(i))
		get_wall_paper(url)

def get_wall_paper(url):
	response = requests.get(url,headers = header)
	selector = parsel.Selector(response.text)
	url = selector.css('.preview::attr(href)').getall()#获取所有图片源地址
	print(url)
	print("当前页面共有{0}张图片".format(len(url)))
	for i in tqdm(url):
		re = requests.get(i,headers=header)
		selector2 = parsel.Selector(re.text)
		url2 = selector2.css('#wallpaper::attr(src)').getall()
		title = selector2.css('title::text').get()
		title = title.split(',')
		for u in url2:
			r = requests.get(u)
			print(r)
			with open(r"./1920x1080/"+title[0]+".jpg","wb") as f:
				f.write(r.content)
				f.close()
				time.sleep(1)
			#print("下载完成请注意查看！！")
if __name__ == '__main__':
	header = {
		'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
	}
	main()
	print("恭喜你！下载已经全部完成了！！")
