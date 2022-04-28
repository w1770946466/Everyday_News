from urllib import request, parse
import requests

class wzry(object):
    def __init__(self):
        self.page = 0  # 抓取的起始页
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}  # 伪装成浏览器

    def get_page(self):
        try:
            while self.page <= 1:   # 设置抓取的结束页
                url = 'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?'\
                      'activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page='+str(self.page) + '&i' \
                      'Order=0&iSortNumClose=1&iAMSAc'\
                      'tivityId=51991&_everyRead=true&iTypeId=2&iFlowId=267733&'\
                      'iActId=2735&iModuleId=2735&_=1554873059538'
                self.page = self.page + 1
                req = request.Request(url, headers=self.headers)
                response = request.urlopen(req)
                #print(response)
                data = response.read()
                #print(data)
                list_data = eval(data)['List']
                #print(list_data)
                for ls in list_data:
                    # 抓取图片url并替换特殊符号
                    sProdImgNo_6 = ls['sProdImgNo_6'].replace('%3A', ':').replace(
                        '%2F', '/').replace('%2E', '.').replace('%5F', '_').replace('%2D', '-').replace('200', '0')
                    sProdName = ls['sProdName']
                    img_name = parse.unquote(sProdName)  # 解码字符串
                    img = requests.get(sProdImgNo_6, verify=False)  # 抓取图片
                    print(f'正在抓取 {img_name} 高清皮肤......')
                    # 写入文件
                    with open(f'./1920x1080/{img_name}.jpg', 'wb') as f:
                        f.write(img.content)
        except request.URLError as e:
            if hasattr(e, 'reason'):
                print(f'抓取失败，失败原因：{e.reason}')


class main():
    wzry().get_page()


if __name__ == '__main__':
    main()
    print('抓取完成。。。')
