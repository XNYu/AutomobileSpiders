#coding=utf-8
import scrapy
import sys
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class ZhipinSpider(scrapy.Spider):
    name = "zhipin"

    def start_requests(self):
        re = scrapy.Request(
            'https://www.zhipin.com/gongsir/2490fc250ee6e9ba1nZ72dW5GQ~~.html?page=1',
            callback=self.parse,
            dont_filter=True)
        yield re

    def parse(self, response):
        ITEMS=[]
        pos = response.xpath("//li//div[@class='job-primary']//div[@class='job-title']/text()").extract()
        price = response.xpath("//li//div[@class='job-primary']//span[@class='red']/text()").extract()
        p = response.xpath("//li//div[@class='job-primary']//p/text()").extract()
        link = response.xpath("//li/a[contains(@href,'job_detail')]/@href").extract()
        for i in range(len(link)):
            link[i] = "https://www.zhipin.com"+link[i]
        print(len(pos),len(price),len(p),len(link))
        for i in range(len(pos)):
            m = i*4
            item = items.jobItem()
            item['position'] = pos[i]
            item['salary'] = price[i]
            item['link'] = link[i+1]
            item['place'] = p[m]
            item['experience'] = p[m+1]
            item['edu'] = p[m+2]
            item['time'] = p[m+3]
            ITEMS.append(item)
            print(item)
        return ITEMS

        print('===============')
        print('===============')
        print('===============')

        # return allCars