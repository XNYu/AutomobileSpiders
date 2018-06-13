#coding=utf-8
import scrapy
import sys
import json
import urllib
import tutorial.Helper.stringHelper as strHelper
import tutorial.Helper.fileHelper as fileHelper
reload(sys)
sys.setdefaultencoding('utf-8')

class LiepinSpider(scrapy.Spider):
    name = "163A"
    def start_requests(self):
            file = open("F:/163links.txt")
            for link in file.readlines():
                link = link.split(",")
                url = link[0]
                comment = link[1]
                re = scrapy.Request(
                    url,
                    callback=self.parseOnePage,
                    dont_filter=True,
                    meta={"comment":strHelper.format(comment)}
                )
                yield re
            file.close()

            # link = "http://auto.163.com/18/0607/08/DJMFNGLF000884MM.html"
            # re = scrapy.Request(
            #     link,
            #     callback=self.parseOnePage,
            #     dont_filter=True,
            #     meta={"comment":"12"}
            # )
            # yield re

    def parseOnePage(self, response):
        pageLink = response.url
        id = response.url.split("/")
        id = id[len(id)-1].split(".h")[0]
        title = strHelper.format(response.xpath("//h1/text()").extract()[0])
        source = response.xpath("//a[@id='ne_article_source']/text()").extract()[0]
        time = response.xpath("//div[@class='post_time_source']/text()").extract()[0]
        time = time.strip().split(" ")[0]
        comment = response.meta['comment']
        contents = response.xpath("//div[@class='post_text']/p")
        pictures=[]
        fulltext = ""
        for content in contents:
            _class= content.xpath("@class").extract()

            if len(_class)>0 and "center" in _class[0]:
                pic = content.xpath("./img/@src").extract_first()
                pictures.append(pic)
                fulltext+="INSERT_PIC_HERE\n"
            else:
                text = content.xpath(".//text()").extract()
                for t in text:
                    fulltext+=t
                fulltext+="\n"

        file = open("F:/163/"+id + ".txt", "w")
        file.write("link: "+pageLink+"\n\n")
        file.write("title: "+title+"\n\n")
        file.write("time: "+time+"\n\n")
        file.write("source: "+source+"\n\n")
        file.write(fulltext+"\n")
        file.write("comment:"+ comment+"\n\n")
        file.write("pic links:")
        for pic in pictures:
            print(pic)
            file.write(pic)
        file.close()
        print('****************************')

# return allCars