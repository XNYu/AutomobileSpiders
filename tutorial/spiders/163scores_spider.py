#coding=utf-8
import scrapy
import sys
import re
import time
import json
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class neteaseScoresSpider(scrapy.Spider):
    name = "scoreN"
    allowed_domains = ["163.com"]
    base_url = "http://product.auto.163.com/review/"
    def start_requests(self):
        file = open('crawled/netease_with_brand.json', 'r')
        file2 = open('crawled/score_netease.json', 'r')
        ids = []
        ids2 = []
        for line in file.readlines():
            dic = json.loads(line)
            webid = dic['web_id']
            ids.append(webid)
        s = set(ids)
        l = list(s)
        l.sort()

        for line in file2.readlines():
            dic = json.loads(line)
            webid = dic['web_id']
            ids2.append(webid)
        s2 = set(ids2)
        l2 = list(s2)
        l2.sort()

        l3 = []
        for ll in l:
            if ll not in l2:
                l3.append(ll)
        print(l3)

        # for id in l3:
        #     yield scrapy.Request("http://product.auto.163.com/review/"+str(id)+".html",self.parse)
        yield scrapy.Request("http://product.auto.163.com/review/" + str(16756) + ".html", self.parse)

    def parse(self, response):
        # outputs title and content of an article
        # title = response.xpath("//h1[@class='main-title']/text()").extract()
        # for s in title:
        #     print(s)
        # content = response.xpath("//font/text()").extract()
        # for m in content:
        #     print(m)
        BandN = response.xpath("//a[@class='menu_name']/text()").extract()
        alterBandN = response.xpath("//div[@class='current-location']/a/text()").extract()
        print(BandN)
        if len(BandN)>1:
            brand = BandN[1]
            name = BandN[2]
        elif len(alterBandN)>1:
            brand = alterBandN[2]
            name = alterBandN[3].split(brand)[1].strip(" ")
        else:
            brand=""
            name=""
        totalScore = response.xpath("//span[@class='total']/strong/text()").extract()[0]
        scorePanel = response.xpath("//div[@id='wangyoupingfen']")[0]
        impressionPanel = response.xpath("//div[@class='lst-yinxiang2']")[0]
        scores = scorePanel.xpath("./div[@class='bd']//span[@class='grade']/text()").extract()
        item = items.scoreItem()
        id = response.url.split("w/")[1].split(".")[0]
        item['web_id'] = id
        item['brand'] = brand
        item['name'] = name
        item['total'] = totalScore
        item['appearance'] = scores[0]
        item['control'] = scores[1]
        item['power'] = scores[1]
        item['comfort'] = scores[2]
        item['repair'] = scores[3]

        impressions = impressionPanel.xpath("//span[@class='yx']/text()").extract()
        impression=""
        if(len(impressions)>1):
            impression = impressions[1]
            if(len(impressions)>2):
                for i in range(2,len(impressions)):
                        impression = impression+","+impressions[i]
        item['impression'] = impression
        # return item
        print('===============')