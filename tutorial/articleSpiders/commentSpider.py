#coding=utf-8
import scrapy
import sys
import json
import os
import re
import tutorial.Helper.stringHelper as strHelper
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class LiepinSpider(scrapy.Spider):
    name = "bb"

    def start_requests(self):
        base_url = "https://reply.autohome.com.cn/showreply/ReplyJson.ashx?id="
        path = "F:/txt"
        list = os.listdir(path)
        for name in list:
            if "all" in name:
                id = name.split("-")[0]
                url = base_url+id
                request = scrapy.Request(
                    url,
                    callback=self.parseComment,
                    dont_filter=True)
                yield request


    def parseComment(self,response):
        id=response.url
        id = id.split("id=")[1]
        print(id)

        jsonBody = response.body.decode('gbk').encode('utf-8')
        jsonBody = jsonBody.split("(")[1].split(")")[0]
        jsonBody = json.loads(jsonBody)
        comment = jsonBody['commentcount']
        file = open("F:/txt/"+id+"-all.txt","a")
        file.write("Comment count:"+ str(comment))
        file.close()

    def parse(self, response):

        print('****************************')
        # print('     |')
        # print('     |')
        # print('     |')
        # print('     |')
        # print('     |')
        # print('     |')
        # print('     |')

# return allCars