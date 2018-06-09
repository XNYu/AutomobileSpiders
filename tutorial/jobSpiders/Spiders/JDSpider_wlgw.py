#coding=utf-8
import scrapy
import sys
import re
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class LiepinSpider(scrapy.Spider):
    name = "jdwlgw"

    def start_requests(self):
        file = open("inputs/wlgw.txt", "r")
        for line in file.readlines():
            line= line.strip()
            re = scrapy.Request(
                line,
                callback=self.parse,
                dont_filter=True)
            yield re


    def parse(self, response):
        item = items.JDItem()
        divs = response.xpath("//input[@type='hidden' and @id='initialHistory']/@value").extract()
        link = response.url
        # print(divs)
        pattern = re.compile('%3E(.*?)%3C')
        patternTime = re.compile('\|!(.*?)!\|')
        dd = pattern.findall(divs[0])
        time = patternTime.findall(divs[0])
        postTime=''
        for t in time:
            if '201' in t:
                postTime = t
        z = False
        r = False
        responsibility=""
        requirement=""
        for rawtext in dd:
            rawtext = rawtext.decode('string-escape').encode('utf-8')
            if "china@nio" in rawtext:
                break
            if "%" in rawtext:
                continue
            if r:
                rawtext = rawtext.strip()
                if len(rawtext) > 0:
                    requirement = requirement + rawtext
            if "要求" in rawtext:
                requirement = rawtext.strip()
                z = False
                r = True
            if z:
                rawtext = rawtext.strip()
                if len(rawtext)>0:
                    responsibility = responsibility + rawtext
            if "职责" in rawtext:
                responsibility = rawtext.strip()
                z = True

        item['time'] = postTime
        item['req'] = requirement
        item['res'] = responsibility
        item['link'] = link
        return item

        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')

# return allCars