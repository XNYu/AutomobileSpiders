#coding=utf-8
import scrapy
import sys
import urllib
from tutorial import items
import json

reload(sys)
sys.setdefaultencoding('utf-8')

class D1evSpider(scrapy.Spider):
    map = {"补贴后售价":"price_after",
           "厂商指导价": "price",
           "用户评分": "score",
           "外观颜色": "color",
           "长宽高": "size",
           "发电机功率": "engine_power",
           "电池容量": "battery_capacity",
           "常规充电": "charge_normal",
           "快速充电": "charge_fast",
           "外观配置": "appearance",
           "电池类型": "battery_type",
           "安全配置": "safety",
           "内饰配置": "interior",
           }

    name = "d1ev"

    def start_requests(self):
        base_url = "http://car.d1ev.com/find/00_2-100_00_00_00_00_00_A.html"
        # base_url = "http://car.d1ev.com/series-17/"
        # base_url = "http://car.d1ev.com/series-79/model-79-265/"
        re = scrapy.Request(
            base_url,
            callback=self.parse,
            dont_filter=True)
        yield re

    def parse(self,response):
        list = response.xpath("//div[@class='pingpai_content']//a/@href").extract()
        for link in list:
            yield scrapy.Request(link,callback=self.parseBrand)

    def parseBrand(self,response):
        list = response.xpath("//ul[@class='content--wrapper am-cf']/li/a/@href").extract()
        brand = response.xpath("//li[@class='am-fl active']//p/text()").extract()[1]
        # brand = response.xpath("//div[@class='conditionList']//span[@class='tag']/text()").extract_first()
        for link in list:
            yield scrapy.Request(link,callback=self.parseModel,meta={"brand":brand})

    def parseModel2(self,response):
        basicinfo = response.xpath("//ol[@class='wrapped am-cf']//li/a/text()").extract()
        brand = response.meta['brand']




    def parseModel(self, response):
        cars = response.xpath("//div[@class='wrapped']//ul[@class='content']/li//a/@href").extract()
        brand = response.meta['brand']
        for car in cars:
            yield scrapy.Request(car,callback=self.parseCar,meta={"brand":brand})

    def parseCar(self, response):
        model_code = response.url.split("-")
        model_code = model_code[len(model_code)-1].split("/")[0]
        print(model_code)
        base_url = "http://car.d1ev.com/web/v1000/cars/carModel/trendPrice.do?modelId="
        url = base_url+str(model_code)+"&city_id=110100"
        u = urllib.urlopen(url)
        price_trend = json.loads(u.read())['data']['listReturnValue']

        item=items.d1Item()
        item['price_trend'] = price_trend
        otherinfo = response.xpath("//ol[@class='wrapped am-cf']//li/a/text()").extract()
        _class = otherinfo[2]
        series = otherinfo[3]
        model = otherinfo[len(otherinfo)-1]
        item["_class"] = _class
        item["model"] = model
        item['series'] = series

        brand = response.meta['brand']
        item["brand"] = brand

        titles = []
        basic = response.xpath("//div[@class='am-cf info_content']//li")
        for list in basic:
            spans = list.xpath(".//span")
            title = spans[0].xpath("./text()").extract_first()
            titles.append(title)
            #encode title for mapping from Chinese to English
            title = self.map[title.encode("utf-8")]
            # get colors
            if "color" in title:
                content = ""
                for i in range(1,len(spans)):
                    content = content+spans[i].xpath("./@style").extract_first().split("d:")[1]
                item["color"] = content

            content = ""
            if len(spans)==2:
                content = spans[1].xpath("./text()").extract_first()
            elif len(spans) == 3:
                content = spans[2].xpath("./text()").extract_first()
            item[title] = content

        adv = response.xpath("//div[@class='config_content']//li[@class]")
        for i in range(0,len(adv)):
            list = adv[i].xpath(".//p")
            if i ==0 or i==3 or i==4:
                content = ""
                for p in list:
                    if "img_tip" not in p.xpath("./@class").extract_first():
                        content = content+ p.xpath("./text()").extract_first() +" "
                    else:
                        title = p.xpath("./text()").extract_first()
                        title = self.map[title.encode("utf-8")]
                        item[title] = content
            elif i ==1:
                content = list[2].xpath("./text()").extract_first().split(" ")
                title = content[0]
                title = self.map[title.encode("utf-8")]
                content = content[1]
                item[title] = content
            elif i ==2:
                continue

        # for dd in item:
        #     print(dd+","+item[dd])
        return item
        # file = open("d1evtitles.txt","w")
        # for t in titles:
        #     file.write(t+" = scrapy.Field()\n")
        # file.close()
        print('****************************')
        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')

# return allCars