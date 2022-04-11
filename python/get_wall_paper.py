import requests
import parsel
import os
import datetime
import random
from tqdm import tqdm


def main():
	pages = []
	while (len(pages)<3): #随机获取10个不相等的
		page = random.randint(1,12380)
		if page not in pages:
			pages.append(page)
	for i in pages:#拼接获取url地址
		url1 = "https://wallhaven.cc/search?categories=110&purity=100&atleast=1920x1080&sorting=date_added&order=desc&page={0}".format(i)#1920x1080是图片比率
		print("正在下载第{0}页所有图片".format(i))
		get_wall_paper(url1)

def get_wall_paper(url):
	response = requests.get(url)
	selector = parsel.Selector(response.text)
	url2 = selector.css('.preview::attr(href)').getall()#获取所有图片源地址
	#print("当前页面共有{0}张图片".format(len(url)))
	for i in tqdm(url2):
		re = requests.get(i)
		selector2 = parsel.Selector(re.text)
		url3 = selector2.css('#wallpaper::attr(src)').getall()
		title = selector2.css('title::text').get()
		title = title.split(',')
		for u in url3:
			print(u)
			r = requests.get(u)
			with open(r"./1920x1080/"+title[0]+".jpg","wb") as f:
				f.write(r.content)
			#print("下载完成请注意查看！！")
if __name__ == '__main__':
	main()
	print("恭喜你！下载已经全部完成了！！")
