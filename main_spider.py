'''
    通过东方财富网爬取上证综指股票信息
    之后进行数据清洗和数据分析
'''
from stock_spider import get_all_url as gurl
from stock_spider import html_downloader as hd
from stock_spider import html_parser as hp
from stock_spider import html_output_csv as ocsv
import random
import time
import os

def go():
    # 实例化对象
    geturl = gurl.get_all_url()
    downloader = hd.html_downloader()
    parser = hp.html_parser()
    output = ocsv.output_csv()

    # 获得所有的股票代码
    code_url_list = geturl.get_url()
    print('一共有{}只股票'.format(len(code_url_list)))
    # 爬虫主循环
    for num, code in enumerate(code_url_list):
        if code + '.csv' in os.listdir('csv'):
            print('第{}个股票数据已经存在'.format(num+1))
            continue
        stock_info = [['日期', '开盘价', '最高价', '最低价', '收盘价', '涨跌额',
                        '涨跌幅(%)', '成交量(手)', '成交金额(万元)', '振幅(%)', '换手率(%)']]
        for year in [2017, 2016, 2015, 2014]:
            for season in [4, 3, 2, 1]:
                # 抓取需要的文本
                text = downloader.downloader(code, str(year), str(season))
                # 抓取需要的信息,并将其加入到列表
                try:
                    stock_info = stock_info + parser.parser(text)
                except Exception as err:
                    print(err)
                # print(stock_info)
        # 将数据写入CSV
        # print(stock_info)
        time.sleep(random.uniform(1, 2))
        output.csv(code, stock_info)
        print('第{}支股票完成'.format(num+1))
    print('全部完成')

# if __name__ =='__main__':
#     go()