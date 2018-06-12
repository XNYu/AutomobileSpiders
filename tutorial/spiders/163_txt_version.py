#coding=utf-8
import scrapy
import sys
import re
from tutorial.Helper import stringHelper as sh

reload(sys)
sys.setdefaultencoding('utf-8')

class SinaSpider(scrapy.Spider):
    name = "163txt"
    allowed_domains = ["163.com"]
    base_url = "http://product.auto.163.com/series/config1/"
    curID=""
    extractedTitle = []
    def start_requests(self):
        # url = "http://product.auto.163.com/series/config1/3148.html"
        # yield scrapy.Request(url,self.parse)
        titleFile = open("inputs/titles.txt", "r")
        for line in titleFile.readlines():
            self.extractedTitle.append(sh.format(line))
        titleFile.close()

        base_url = "http://product.auto.163.com/series/config1/"
        file = open("F:/ids.txt","r")
        # i=0
        for line in file.readlines():
            # if i<2:
            #     i+=2
            # else:
            #     break
            id = sh.format(line)
            url = base_url+id+".html"
            request = scrapy.Request(url,self.parse)
            yield request
        file.close()


    def stringStrip(self,att):
        # att = att.decode("string-escape")
        att = att.strip()
        att = att.replace("\t", "")
        att = att.replace("\r", "")
        att = att.replace("\n", "")
        att = att.replace(" ", "")
        return att

    def parse(self, response):
        error = response.xpath("//div[@id='nav_hd']")
        if(error):
            return
        attributes = ['year', 'engine', 'product_id', 'product_name', 'price']
        attributes2 = ['year', 'engine', 'product_id', 'product_name', 'price', 'brand', 'web_id', 'link']
        basic = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i',]
        brand = response.xpath("//a[@class='menu_name']/text()").extract()
        product_brand = brand[1]
        product_name = brand[2]
        attrnames = response.xpath("//div[@class='car_config_param_names']/div")
        allCars = []
        # names = ""
        # for n in attrnames:
        #     names+=" "+n
        # print(names)
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

        dicts = []
        for number in range(0, carCount):
            dddd = {}
            dicts.append(dddd)
        index=0
        start=False
        basicAttributes = response.xpath("//div[@class='car_config_param_list']/div")
        # print(len(basicAttributes))
        countDown = 0
        curAttrs ={}
        count=0
        titles=[]
        for i in range(0,len(basicAttributes)):
            _attribute = basicAttributes[i]
            _title = attrnames[i]
            _class = _title.xpath("./@class").extract_first()
            if "head" in _class:
                continue
            count+=1
            _titleN = _title.xpath(".//span/@title").extract_first()
            titles.append(_titleN)
            spans = _attribute.xpath(".//span/text()").extract()
            for j in range(0, len(allCars)):
                text = spans[j]
                if "●" in text:
                    text = "标配"
                if "○" in text:
                    text = "选配"
                allCars[j][_titleN] = sh.format(text)
        fulltext = ""
        for i in range(0,len(allCars)):
            for att in attributes2:
                fulltext = fulltext + att+ "="+sh.format(allCars[i][att])+"$"
            for dd in self.extractedTitle:
                if dd in allCars[i].keys():
                    fulltext = fulltext + dd + "=" + allCars[i][dd.decode('utf-8')] + "$"
                else:
                    fulltext = fulltext+dd+"=--$"
        print(count)

        # file = open("inputs/titles.txt","w")
        # for t in titles:
        #     file.write(t+" = scrapy.Field()\n")
        # file.close()

        file = open("crawled/163.txt","a")
        file.write(fulltext+"\n")
        file.close()
        # return allCars

        print('===============')