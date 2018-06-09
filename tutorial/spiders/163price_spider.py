#coding=utf-8
import scrapy
import sys
import re
import time
import json
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class neteasePriceSpider(scrapy.Spider):
    name = "priceN"
    allowed_domains = ["163.com"]
    base_url = "http://product.auto.163.com/product/"
    ids = {}
    def start_requests(self):
        # yield scrapy.Request('http://k.sina.com.cn/article_6407646347_17decec8b00100680d.html',self.parse)
        # yield scrapy.Request('http://db.auto.sina.com.cn/660/peizhi/',self.parse)
        # yield scrapy.Request('http://price.pcauto.com.cn/sg3225/config.html',self.parse)
        file = open('netease_with_brand.json', 'r')

        for line in file.readlines():
            dic = json.loads(line)
            ida = dic['product_id']
            brand = dic['brand']
            self.ids[ida] = brand
        for id in self.ids:
            yield scrapy.Request("http://product.auto.163.com/product/"+id+".html",self.parse)

            # time.sleep(0.05)
        # for id in range(18000, 23000):
        #     time.sleep(1)
        #     yield scrapy.Request('http://product.auto.163.com/series/config1/' + str(id) + '.html', self.parse)

    def parse(self, response):
        # outputs title and content of an article
        # title = response.xpath("//h1[@class='main-title']/text()").extract()
        # for s in title:
        #     print(s)
        # content = response.xpath("//font/text()").extract()
        # for m in content:
        #     print(m)
        attrs = response.xpath("//span[@class='red']/big/text()").extract()[0]
        name = response.xpath("//div[@class='brand_box']/h1/text()").extract()[0]
        title = response.xpath("//h2[@class='brand_title']/span/a/text()").extract()[0]
        item = items.priceItem()
        id = response.url.split("ct/")[1].split(".")[0]
        item['brand'] = self.ids[id]
        item['name'] = title+" "+name
        item['id'] = id
        item['price'] = attrs
        item['source'] = 'netease'
        return item
        # i=0;
        # for s in response.xpath("//div[@class='car_config_param_names']"
        #                         "//span[@class='cell_text']/text()").extract():
        #     i=i+1
        #     if i>12:break
        #     print(s)
        print('===============')
        # return allCars