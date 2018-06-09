#coding=utf-8
import scrapy
import sys
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class LiepinSpider(scrapy.Spider):
    name = "yiche"

    def start_requests(self):
        base_url = "http://car.bitauto.com/tree_chexing/mb_9/"
        re = scrapy.Request(
            base_url,
            callback=self.parse,
            dont_filter=True)
        yield re

    def parse(self, response):
        ITEMS=[]
        text = response.xpath("//div[@class='tree-list']/div").extract()
        print(len(text))
        # for t in text:
        #     l = text.xpath(".//a")
        #     link = l.xpath("./@href").extract_first()
        #     print(link)
        print(text)

        print('****************************')

# return allCars