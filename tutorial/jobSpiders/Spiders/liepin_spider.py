#coding=utf-8
import scrapy
import sys
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class LiepinSpider(scrapy.Spider):
    name = "liepin"

    def start_requests(self):
        base_url = "https://www.liepin.com/zhaopin/?pubTime=&ckid=" \
                   "4426235589b22cb2&fromSearchBtn=2&compkind=&isAnal" \
                   "ysis=&init=-1&searchType=1&dqs=&industryType=&jobKind" \
                   "=&sortFlag=15&degradeFlag=0&industries=&salary=&comps" \
                   "cale=&key=%E5%A8%81%E9%A9%AC%E6%B1%BD%E8%BD%A6&clean_" \
                   "condition=&headckid=4426235589b22cb2&d_pageSize=40&siT" \
                   "ag=Tixmjjrqbpigr3dNc0BLfw~fA9rXquZc5IkJpXC-Ycixw&d" \
                   "_headId=b1eee833a69e5f34e7861c0a0fb81d19&d" \
                   "_ckId=b1eee833a69e5f34e7861c0a0fb81d19&d_sfrom=search_fp&d_" \
                   "curPage=0&curPage="
        for i in range(0,10):
            url = base_url+ str(i)
            re = scrapy.Request(
                url,
                callback=self.parse,
                dont_filter=True)
            yield re

    def parse(self, response):
        ITEMS=[]
        table = response.xpath("//div[@class='job-info']")
        for info in table:
            item = items.jobItem()
            # print(info)
            title = info.xpath(".//a[@data-promid]")
            link = title.xpath("./@href").extract_first()
            position = title.xpath("./text()").extract_first().strip()
            information = info.xpath(".//p[@class='condition clearfix']/@title").extract_first()
            information = information.split("_")
            time = info.xpath(".//time/text()").extract_first()
            item['link'] = link
            item['position']=position
            item['salary'] = information[0]
            item['place'] = information[1]
            item['edu'] = information[2]
            item['experience'] = information[3]
            if '分钟' in time or '小时' in time:
                time = '2018-05-24'
            item['time'] = time
            ITEMS.append(item)
            # for d in item:
            #     print(d+","+item[d])
            # print(time)
        return ITEMS





        # pos = response.xpath("//li//div[@class='job-primary']//div[@class='job-title']/text()").extract()
        # price = response.xpath("//li//div[@class='job-primary']//span[@class='red']/text()").extract()
        # p = response.xpath("//li//div[@class='job-primary']//p/text()").extract()
        # link = response.xpath("//li/a[contains(@href,'job_detail')]/@href").extract()
        # for i in range(len(link)):
        #     link[i] = "https://www.zhipin.com"+link[i]
        # print(len(pos),len(price),len(p),len(link))
        # for i in range(len(pos)):
        #     m = i*4
        #     item = items.jobItem()
        #     item['position'] = pos[i]
        #     item['salary'] = price[i]
        #     item['link'] = link[i+1]
        #     item['place'] = p[m]
        #     item['experience'] = p[m+1]
        #     item['edu'] = p[m+2]
        #     item['time'] = p[m+3]
        #     ITEMS.append(item)
        #     print(item)
        # return ITEMS

        print('===============')
        print('     |')
        print('     |')

        print('     |')

        print('     |')

        print('     |')

        print('     |')

        print('     |')

# return allCars