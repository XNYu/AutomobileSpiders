#coding=utf-8
import scrapy
import sys
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class LiepinSpider(scrapy.Spider):
    name = "koubei"

    def start_requests(self):
        base_url = "https://k.autohome.com.cn/detail/view_01ce318yj068r36dhj68t00000.html?st=1&piap=0|2123|0|0|1|0|0|0|0|0|1#pvareaid=2112108"
        re = scrapy.Request(
            base_url,
            callback=self.parse,
            dont_filter=True)
        yield re

    def parse(self, response):
        ITEMS=[]
        text = response.xpath("//div[@class='text-con']")[0].extract()
        print(text)

        print('****************************')
        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')
        print('     |')

# return allCars