import requests
from bs4 import BeautifulSoup
import re

class get_all_url(object):
    def get_url(self):
        url = 'http://quote.eastmoney.com/stocklist.html#sh'
        header = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        }
        r = requests.get(url, headers=header, timeout=2)
        soup = BeautifulSoup(r.text, 'html.parser')
        primary_stock_code = soup.find('div',{'class':'quotebody'}).select('li')
        # print(primary_stock_code)
        code_url_list = []
        for every_stock in primary_stock_code:
            # 获得股票对于的网址
            # stock_url = every_stock.find('a',{'target':'_blank'})['href']
            stock_code = every_stock.text
            # .group()只获取需要的代码数字
            stock_code = re.search(r'\d{6}', stock_code).group()
            if int(stock_code[0]) in [0,3,6]:
                # code_url_list.append([stock_url, stock_code])
                code_url_list.append(stock_code)
        # print(code_url_list)
        print('URL和股票代码成功获得')
        return code_url_list

