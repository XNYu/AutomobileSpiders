#coding=utf-8
import scrapy
import sys
import re
import time
import json
from tutorial.Helper import stringHelper as sh
from tutorial import items
import tutorial.Helper.jsonHelper as jh

reload(sys)
sys.setdefaultencoding('utf-8')

dict = jh.getDict()

class SinaSpider(scrapy.Spider):
    name = "163"
    allowed_domains = ["163.com"]
    base_url = "http://product.auto.163.com/series/config1/"
    curID=""
    def start_requests(self):
        # yield scrapy.Request('http://k.sina.com.cn/article_6407646347_17decec8b00100680d.html',self.parse)
        # yield scrapy.Request('http://db.auto.sina.com.cn/660/peizhi/',self.parse)
        # yield scrapy.Request('http://price.pcauto.com.cn/sg3225/config.html',self.parse)
        url = "http://product.auto.163.com/series/config1/2005.html"
        yield scrapy.Request(url,self.parse)
        # base_url = "http://product.auto.163.com/series/config1/"
        # file = open("F:/ids.txt","r")
        # i=0
        # for line in file.readlines():
        #     id = sh.format(line)
        #     url = base_url+id+".html"
        #     request = scrapy.Request(url,self.parse)
        #     yield request
        # file.close()

        # request = scrapy.Request("http://product.auto.163.com/series/config1/18709.html",self.parse)
        # yield request

    def stringStrip(self,att):
        # att = att.decode("string-escape")
        att = att.strip()
        att = att.replace("\t", "")
        att = att.replace("\r", "")
        att = att.replace("\n", "")
        att = att.replace(" ", "")
        return att

    def parse(self, response):
        # outputs title and content of an article
        # title = response.xpath("//h1[@class='main-title']/text()").extract()
        # for s in title:
        #     print(s)
        # content = response.xpath("//font/text()").extract()
        # for m in content:
        #     print(m)
        error = response.xpath("//div[@id='nav_hd']")
        if(error):
            return
        attributes = ['year', 'engine', 'product_id', 'product_name', 'price']
        basic = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i',]
        brand = response.xpath("//a[@class='menu_name']/text()").extract()
        product_brand = brand[1]
        product_name = brand[2]
        attrnames = response.xpath("//div[@class='car_config_param_names']//span/text()").extract()
        allCars = []
        names = ""
        for name in attrnames:
            names+=" "+name
        print(names)
        print(len(attrnames))



        #outputs product basic information\
        cars = response.xpath("//div[@class='car_config_param_head']//div[@class='cell']")
        for car in cars:
            for y in car.xpath("./@data-config").extract():
                x = y.decode("string-escape")
                mm = x.split(",")
                pattern = re.compile("'(.*)'")
                item = {}
                for i in range(len(mm)):
                    item[attributes[i]] = pattern.findall(mm[i])[0]
                fullname = ""
                for name in car.xpath(".//a[@target='_blank']/text()").extract():
                    fullname = fullname + " " + name
                item['product_name'] = fullname
                item['brand'] = product_brand
                item['web_id'] = response.url.split("g1/")[1].split(".")[0]
                item['link'] = response.url
                allCars.append(item)
        carCount = len(allCars)


        # data = response.xpath("//div[@class='car_config_param_names']//div[@class='row_head']")
        # file = open("types.txt","w")
        # for d in data:
        #     id = d.xpath("./@id").extract_first()
        #     text = d.xpath(".//span/text()").extract_first()
        #     file.write(id+"\n")
        #     file.write(text+"\n")
        types = ["24","14","21","22","16","18","31","23","28","29",
                 "218","219","27","25","30","32","221","220"]
        numberTOWord ={"14":"Basic",
                       "21":"Body",
                       "16": "Engine",
                       "220": "Motor",
                       "221": "Battery",
                       "22": "Drive",
                       "23": "Chassis",
                       "218": "Wheel",
                       "24": "Safety",
                       "25": "Control",
                       "18": "Exterior",
                       "26": "Interior",
                       "27": "Light",
                       "28": "Glass",
                       "29": "AC",
                       "30": "Seat",
                       "31": "Multimedia",
                       "219": "Color",
                       "32": "Others",}

        dicts = []
        for number in range(0, carCount):
            dddd = {}
            dicts.append(dddd)
        index=0
        curType=""
        start=False
        basicAttributes = response.xpath("//div[@class='car_config_param_list']//div")
        # print(len(basicAttributes))
        countDown = 0
        curAttrs ={}

        for name in dict:
            for i in range(0, len(dict[name])):
                dict[name][i] = dict[name][i].decode()
        indexInType = -1
        for it in basicAttributes:
            countDown+=1
            if(countDown<0):
                break

            _class = it.xpath("./@class").extract_first()

            if(_class=='row_head'):
                indexInType = -1
                if start:
                    for carIndex in range(0,carCount):
                        strings = json.dumps(dicts[carIndex],encoding='utf-8',ensure_ascii=False)
                        # print(strings)
                        allCars[carIndex][numberTOWord[id]] = strings
                        dicts[carIndex] = {}
                id = it.xpath('./@id').extract_first()
                id = id +""
                curAttrs = dict[id]

            if(_class=='cell'):
                row = it.xpath("./span[@class='cell_text']/text()").extract_first()
                row= self.stringStrip(row)
                curIndex = index%carCount
                index+=1
                if(curIndex==0):
                    indexInType = indexInType + 1
                curType = curAttrs[indexInType]
                dicts[curIndex][curType] = row.encode('utf-8')
                start = True

        # return allCars

        print('===============')