import csv

class output_csv(object):
    def csv(self, stock_code, stock_list):
        # print(stock_list)
        with open('csv/'+ stock_code +'.csv', 'w',encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for list in stock_list:
                writer.writerow(list)
        # print('csv写入成功')


