#coding=utf-8
import scrapy
import sys
import re
import time
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class SinaSpider(scrapy.Spider):
    name = "netease"
    allowed_domains = ["163.com"]
    base_url = "http://product.auto.163.com/series/config1/"
    curID=""
    def start_requests(self):
        # yield scrapy.Request('http://k.sina.com.cn/article_6407646347_17decec8b00100680d.html',self.parse)
        # yield scrapy.Request('http://db.auto.sina.com.cn/660/peizhi/',self.parse)
        # yield scrapy.Request('http://price.pcauto.com.cn/sg3225/config.html',self.parse)
        request = scrapy.Request("http://product.auto.163.com/series/config1/18810.html#0008H31",self.parse)
        yield request
        # for id in range (1900,20000):
        #     if id>5000 and id<15000: continue
        #     request = scrapy.Request('http://product.auto.163.com/series/config1/'+ str(id) +'.html',self.parse)
        #     # request.meta['id'] = id
        #     yield request
        #     # time.sleep(0.05)
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
        error = response.xpath("//div[@id='nav_hd']")
        if(error):
            return
        attributes = ['year', 'engine', 'product_id', 'product_name', 'price']
        basicAttr = ['manufactor','carStructure','size','engine','gearbox','maximumSpeed'
            ,'accelerationTime','fuelConsumption','warranty','maintenanceInterval','powerType']
        allCars = []
        #outputs product basic information\

        brand = response.xpath("//a[@class='menu_name']/text()").extract()
        product_brand = brand[1]

        cars = response.xpath("//div[@class='car_config_param_head']//div[@class='cell']")
        for car in cars:
            for y in car.xpath("./@data-config").extract():
                 x = y.decode("string-escape")
                 mm = x.split(",")
                 pattern = re.compile("'(.*)'")
                 item = items.CarItem()
                 for i in range(len(mm)):
                     item[attributes[i]] = pattern.findall(mm[i])[0]
                 fullname=""
                 for name in car.xpath(".//a[@target='_blank']/text()").extract():
                     fullname = fullname+" "+name
                 item['product_name'] = fullname
                 item['brand'] = product_brand
                 item['web_id'] = response.url.split("g1/")[1].split(".")[0]
                 allCars.append(item)

        basicAttributes = response.xpath("//div[@class='car_config_param_list']//div[@class='row']")
        i=0;
        for attr in basicAttributes:
            if i>10:break
            row = attr.xpath(".//span[@class='cell_text']/text()").extract()
            # print(row)
            for index in range(0,len(allCars)):
                att = row[index]
                att = att.decode("string-escape")
                att = att.strip()
                att = att.replace("\t","")
                att = att.replace("\r","")
                att = att.replace("\n","")
                att = att.replace(" ","")
                allCars[index][basicAttr[i]] = att
                # print(att)
            i = i + 1;
        print(allCars[0])
        # i=0;
        # for s in response.xpath("//div[@class='car_config_param_names']"
        #                         "//span[@class='cell_text']/text()").extract():
        #     i=i+1
        #     if i>12:break
        #     print(s)
        print('===============')
        # return allCars