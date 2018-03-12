import csv
import pymysql
import os
import warnings
# 取消警告
warnings.filterwarnings("ignore")
# 获得csv文件名
codelist = os.listdir('newcsv/')
connect = pymysql.connect(host="localhost",
                          user="root",
                          password="199571",
                          db="stock_info",
                          port=3306)
cur = connect.cursor()
cur.execute("use stock_info")

for i, list in enumerate(codelist):
    table = 'stock' + list.split('.')[0]
    cur.execute("drop table if exists {}".format(table))  # 如果表存在则删除
    sql = """create table {}(day DATE, opening_price FLOAT, highest_price FLOAT, lowest_price FLOAT, 
        closed_price FLOAT, ups_and_downs FLOAT,ups_and_downs_percent FLOAT, volume FLOAT, trading_amount FLOAT,
        amplitude_percent FLOAT, rate_to_turnover_percent FLOAT)""".format(table)  # ()中的参数可以自行设置
    # 去除sql中的换行符
    cur.execute(''.join(sql.split('\n')))  # 创建表，定义表中数据类型
    try:
        with open('newcsv/'+'{}.csv'.format(list.split('.')[0]), 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                # 写入mysql的日期需要加引号，如 '2014-04-04'
                line[0] = '\'' + line[0] + '\''
                b = '#'.join(line)
                # 部分数字有‘，’分隔，去除这种数字中的逗号
                c = b.replace(',', '').replace('#', ',')
                a = 'INSERT INTO {} VALUE('.format(table) + c + ')'
                # 插入数据
                cur.execute(a)
            connect.commit()
    except Exception as err:
        print('{}表创建失败'.format(table))
        print(err)
cur.close()  # 关闭游标连接
connect.close()  # 关闭数据库服务器连接 释放内存
print('Mission completed!')

