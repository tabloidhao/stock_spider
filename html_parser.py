from bs4 import BeautifulSoup

class html_parser(object):
    def parser(self, text):
        if text is None:
            print('网页内容为空，返回None')
            return None
        soup = BeautifulSoup(text, 'html.parser')
        # 找到大标签下的小标签
        stock = soup.find('table',{'class':'table_bg001 border_box limit_sale'})
        stock = stock.find_all('tr')

        stock_info = []
        # 将股票数据添加到文本
        for num in stock:
            stock_body_list = []
            txt = num.select('td')
            for r in txt:
                # bs的.text不能用在列表上
                stock_body_list.append(r.text)
            stock_info.append(stock_body_list)
        # print(stock_info[1:])
        # print('数据存储成功')
        # 列表第一个是空的
        return stock_info[1:]















# 正则匹配失败
# print(r.text)
# a = re.search(r'[1-2]\d*.\d*|0.\d*[1-9]\d*', r).group(0)
# if a is None:
#     a = re.search(r'\d{4}(\-|\/|.)\d{1,2}\1\d{1,2}', r).group(0)
#     if a is None:
#         a = re.search(r'-([1-2]\d*.\d*|0.\d*[1-9]\d*)', r).group(0)
# if stock_body_list is not None:
# stock_body_list.append(r_list)