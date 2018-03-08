import requests

class html_downloader(object):
    def downloader(self, stock_code, year, season):
        header = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        }
        # 构建URL
        # url = 'http://quotes.money.163.com/trade/lsjysj_000001.html?year=2016&season=1'
        url = 'http://quotes.money.163.com/trade/lsjysj_' + stock_code + '.html'
        parser = {'year':year,'season':season}
        try:
            r = requests.get(url, params=parser, headers=header, timeout= 5)
            # print(r.url)
            # print('网页抓取成功')
            return r.text
        except Exception as err:
            print(err)
            print('网页抓取失败')
            return None