#coding=utf-8
import scrapy
import sys
import re
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class LiepinSpider(scrapy.Spider):
    name = "jdwlboss"

    def start_requests(self):
        file = open("inputs/wlboss.txt", "r")
        for line in file.readlines():
            line= line.strip()
            re = scrapy.Request(
                line,
                callback=self.parse,
                dont_filter=True)
            yield re


    def parse(self, response):
        item = items.JDItem()
        divs = response.xpath("//div[@class='text']/text()").extract()
        link = response.url
        start=False
        zz = False
        yq = False
        req= ""
        res= ""
        for dd in divs:
            dd = dd.strip()
            dd = dd.replace("\r","")
            dd = dd.replace("\n","")
            if "关于" in dd:
                break
            if yq:
                req = req + ' ' +dd
            if "要求" in dd:
                req= '"'+dd
                zz=False
                yq=True
            if zz:
                res = res + " "+ dd
            if "职责" in dd:
                res = dd
                zz=True
        item['req'] = req
        item['res'] = res
        item['link'] = response.url
        return item
        # z = False
        # r = False
        # responsibility=""
        # requirement=""
        # for rawtext in divs:
        #     rawtext = rawtext.decode('string-escape').encode('utf-8')
        #     if "china@nio" in rawtext:
        #         break
        #     if "%" in rawtext:
        #         continue
        #     if r:
        #         rawtext = rawtext.strip()
        #         if len(rawtext) > 0:
        #             requirement = requirement + rawtext
        #     if "要求" in rawtext:
        #         requirement = rawtext.strip()
        #         z = False
        #         r = True
        #     if z:
        #         rawtext = rawtext.strip()
        #         if len(rawtext)>0:
        #             responsibility = responsibility + rawtext
        #     if "职责" in rawtext:
        #         responsibility = rawtext.strip()
        #         z = True
        #
        # item['time'] = postTime
        # item['req'] = requirement
        # item['res'] = responsibility
        # item['link'] = link
        # return item

        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')

# return allCars