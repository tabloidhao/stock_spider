import re
import requests
import threading
import csv
from bs4 import BeautifulSoup

# 股票代码对应的URL
STOCK_URL_LIST = []
# 股票代码
CODE_LIST = []
gLock = threading.Lock()

def get_all_url():
    # 获得所有股票的代码
    code_url = 'http://quote.eastmoney.com/stocklist.html#sh'
    header = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    }
    r = requests.get(code_url, headers=header, timeout=5)
    soup = BeautifulSoup(r.text, 'html.parser')
    primary_stock_code = soup.find('div', {'class': 'quotebody'}).select('li')
    for every_stock_code in primary_stock_code:
        stock_code = every_stock_code.text
        stock_code = re.search(r'\d{6}', stock_code).group()        # .group()只获取需要的代码数字
        if int(stock_code[0]) in [0, 3, 6]:
            CODE_LIST.append(stock_code)

def producer():
    # 生成所有要爬取的URL
    while True:
        if len(CODE_LIST) == 0:
            print('一共有{}个URL'.format(len(STOCK_URL_LIST)))
            print('生产完成')
            return None
        stock_code = CODE_LIST.pop()
        former_url = 'http://quotes.money.163.com/trade/lsjysj_'
        STOCK_URL_LIST.append(former_url + stock_code + '.html' + '?year=2018&season=1')
        for year in [2017, 2016, 2015, 2014]:
            for season in [4, 3, 2, 1]:
                true_url = former_url + stock_code + '.html' + '?year='+str(year)+'&season='+str(season)
                STOCK_URL_LIST.append(true_url)

def comsumer():
    # 抓取股票信息并保存
    while True:
        header = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        }
        gLock.acquire()
        if len(STOCK_URL_LIST) == 0:
            gLock.release()
            break
        url = STOCK_URL_LIST.pop()
        gLock.release()
        try:
            r = requests.get(url, headers=header)
            # 解析网页
            soup = BeautifulSoup(r.text, 'html.parser')
            stock = soup.find('table', {'class': 'table_bg001 border_box limit_sale'})
            stock = stock.find_all('tr')
            stock_info = []
            # 将股票数据添加到文本
            for num in stock:
                stock_body_list = []
                txt = num.select('td')
                for r in txt:
                    stock_body_list.append(r.text)          # bs的.text不能用在列表上
                stock_info.append(stock_body_list)
            code = re.search(r'\d{6}', url).group()         # 正则获取股票代码
            with open('newcsv/' + code + '.csv', 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                for list in stock_info[1:]:
                    writer.writerow(list)
                print('{}股票存储中'.format(code))
        except Exception as err:
            print(err)
            print('网页抓取失败')

def main():
    get_all_url()
    producer()
    # 同时进行5个进程，校园网跑满只有1M，垃圾学校。
    for i in range(5):
        th = threading.Thread(target=comsumer)
        th.start()

if __name__=='__main__':
    main()