#coding=utf-8
import scrapy
import sys
import re
import time
import json
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class autoScoreSpider(scrapy.Spider):
    name = "scoreA"
    allowed_domains = ["autohome.com.cn"]
    ids = {}
    def start_requests(self):
        file = open('crawled/id_autohome.json', 'r')
        ids = []
        for line in file.readlines():
            dic = json.loads(line)
            id = dic['id']
            ids.append(id)
        i = 0
        for id in ids:
            yield scrapy.Request("https://www.autohome.com.cn/"+str(id)+"/",self.parse)
            i=i+1
            # time.sleep(0.05)

    def parse(self, response):
        item = items.scoreItem()
        total = response.xpath("//a[@class='font-score']/text()").extract()
        if len(total)>0:
            item['total'] = total[0]
        attributes=['space','power','control','fuel','comfort','appearance','interior','costperformance']

        brand = response.xpath("//div[@class='subnav-title-name']/a/text()").extract()
        name = response.xpath("//div[@class='subnav-title-name']/a/h1/text()").extract()
        if len(brand)<1:return
        if len(name)<1:return
        brand = brand[0]
        name = name[0]
        brand = brand.strip("-")
        id = response.url.split("/")[3]

        table = response.xpath("//table[@class='table-rank']")
        if len(table)<1:
            return
        tr = table.xpath("./tr")
        for i in range(len(tr)):
            score =  tr[i].xpath("./td/a/text()").extract()[0]
            score = score[0:len(score)-1]
            item[attributes[i]] = score
        item['brand'] = brand
        item['name'] = name
        item['web_id'] = id
        item['source'] = 'autohome'
        print('===============')
        return item