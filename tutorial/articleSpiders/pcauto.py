#coding:utf-8
import scrapy
import sys
import json
import urllib
from tutorial.Helper import fileHelper as fileHelper
import tutorial.Helper.stringHelper as strHelper

class LiepinSpider(scrapy.Spider):
    name = "pc"
    def start_requests(self):

        # url = "https://www.autohome.com.cn/use/201711/909485.html#pvareaid=102624"
        # base_url = "http://auto.sina.com.cn/service/?page="

        # yield scrapy.Request(url,self.parseOnePage)
        # base_url = "http://auto.sina.com.cn/j_kandian.d.html?docid=fyremfz2599182"
        link = 'http://www.pcauto.com.cn/drivers/yangche/point/'
        # re = scrapy.Request(
        #     strHelper.format(link),
        #     callback=self.parseHome,
        #     dont_filter=True
        # )
        # yield re
        for i in range(9,11):
            re = scrapy.Request(
                strHelper.format(link)+"index_"+str(i)+".html",
                callback=self.parseHome,
                dont_filter=True
            )
            yield re

    def parseHome(self,response):
        links = response.xpath("//div[@class='pic-txt clearfix']")
        for l in links:
            link = l.xpath(".//a/@href").extract_first()
            print(link)
            yield scrapy.Request(link, self.parse)

    def parse(self, response):
        page_link = response.url

        more_pages = response.xpath("//div[@class='pcauto_page']")
        if len(more_pages)>0:
            new_link = page_link.replace(".html","_all.html")
            yield scrapy.Request(new_link,self.parseOnePage)
        else:
            yield scrapy.Request(page_link,self.parseOnePage)

    def parseComment(self,response):
        jsonBody =json.loads(response.body.decode('gbk').encode('utf-8'))
        comment = jsonBody["total"]
        print(comment)
        id = response.url.split("/")
        id = id[len(id) - 1].split(".html")[0]
        file = open("F:/pcauto/" + id + ".txt", "a")
        comment = "Comment:" + str(comment) + "\n"
        file.write(comment)
        file.close()

    def parseOnePage(self,response):
        page_link = response.url.replace("_all","")
        base_link = "http://cmt.pcauto.com.cn/action/topic/get_data.jsp?url="
        yield scrapy.Request(base_link + page_link, self.parseComment)

        id = page_link.split("/")
        id = id[len(id) - 1].split(".html")[0]

        title = response.xpath("//h1[@class='artTit']/span/text()").extract_first()
        title = strHelper.format(title)
        source = response.xpath("//span[@class='ownner']/text()").extract_first()
        source = strHelper.format(source)
        author = strHelper.format(response.xpath("//span[@class='editor']//a/text()").extract_first())
        time = strHelper.format(response.xpath("//span[@class='pubTime']/text()").extract_first())
        mark = response.xpath("//p[@class='moreRead artTag']//a/text()").extract()
        marks =""
        for m in mark:
            marks+=m+","
        marks = marks[0:len(marks)-1]
        # print(title)
        # print(source)
        # print(author)

        contents = response.xpath("//div[@class='artText clearfix']")
        contents = contents.xpath(".//p|.//div[@class='cmsArtMainTit']")
        pictures=[]
        fulltext=""
        for block in contents:
            if len(block.xpath("./@class"))>0:
                fulltext+=block.xpath(".//text()").extract_first() + "\n"
            elif len(block.xpath("./@style"))>0:
                fulltext+="INSERT_PIC_HERE\n\n"
                pic = block.xpath(".//img/@src").extract_first()
                pictures.append(pic)
            else:
                text=block.xpath(".//text()").extract()
                for t in text:
                    fulltext+=t
                fulltext+="\n"

        picCount = 0
        # for link in pictures:
            # Create folder for each document
            # fileHelper.mkdir(id)
            # print(link)
            # if link is None:
            #     continue
            # urllib.urlretrieve(link, "F:/sina/images/" + id + "/" + str(picCount) + ".webp")
            # picCount += 1
        # print("Get pic :" + str(picCount))
        # print(fulltext)
        file = open("F:/pcauto/"+id+".txt","w")
        file.write("link: "+page_link+"\n\n")
        file.write("title: "+title+"\n\n")
        file.write("time: "+time+"\n\n")
        file.write("source: "+source+"\n\n")
        file.write("tag:" + marks + "\n\n")
        file.write(fulltext+"\n")
        file.close()