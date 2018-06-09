#coding:utf-8
import jsonHelper as jh
import pymongo

host = '127.0.0.1'
port = 27017
dbname = 'scrapy'
sheetname = 'netease'
# 创建MONGODB数据库链接
client = pymongo.MongoClient(host=host, port=port)
# 指定数据库
mydb = client[dbname]
# 存放数据的数据库表名
net = mydb[sheetname]

net.insert({"1":1})
# for dd in d1:
#     for mm in dd:
#         print(mm+","+dd[mm])