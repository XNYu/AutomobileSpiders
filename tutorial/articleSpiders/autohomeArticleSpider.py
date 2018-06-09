#coding=utf-8
import scrapy
import sys
import json
import urllib
from tutorial.Helper import fileHelper as fileHelper
import tutorial.Helper.stringHelper as strHelper
import os
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class LiepinSpider(scrapy.Spider):
    name = "aa"
    def start_requests(self):

        # url = "https://www.autohome.com.cn/use/201711/909485.html#pvareaid=102624"
        base_url = "https://www.autohome.com.cn/use/"

        # yield scrapy.Request(url,self.parseOnePage)
        for i in range(26,28):
            re = scrapy.Request(
                base_url+str(i)+"/",
                callback=self.parse,
                dont_filter=True)
            yield re

    def parse(self,response):
        articles = response.xpath("//div[@id='auto-channel-lazyload-article']//ul[@class='article']")
        for block in articles:
            links = block.xpath(".//a/@href").extract()
            for link in links:
                link = "https:"+link
                yield scrapy.Request(link,self.parseOnePage)

    def getID(self,str):
        str = str.split(".html")[0]
        str = str.split("/")[5]
        return str

    def parseComment(self,response):
        jsonBody = response.body.decode('gbk').encode('utf-8')
        jsonBody = jsonBody.split("(")[1].split(")")[0]
        jsonBody = json.loads(jsonBody)
        commentCount = jsonBody['commentcount']
        id = response.url.split("id=")[1]
        file = open("txt/"+id+".txt","a")
        comment = "Comment count:" + str(commentCount)+"\n"
        file.write(comment)
        file.close()

    def parseOnePage(self, response):
        originurl = response.url
        id = self.getID(originurl)

        nextpage = response.xpath("//div[@class='athm-page__info']")
        if len(nextpage)>0:
            if "all" not in id:
                newID = id+"-all.html"
                yield scrapy.Request("https://www.autohome.com.cn/use/201803/"+newID,self.parseOnePage)
                return

        details = response.xpath("//div[@class='article-details']")

        marks = details.xpath(".//div[@class='marks']/a/text()").extract_first()
        if marks is None:
            marks = ""
        title = details.xpath("//h1/text()").extract_first()
        title = strHelper.format(title)
        author = details.xpath("//a[@class='name']/text()").extract_first()
        author = strHelper.format(author)
        time = details.xpath("//span[@class='time']/text()").extract_first()
        time = strHelper.format(time)
        source = details.xpath("//span[@class='source']/a/text()").extract_first()
        source = strHelper.format(source)
        pageLink = response.url
        commentjsonurl = "https://reply.autohome.com.cn/showreply/ReplyJson.ashx?id="


        commentjsonurl+=id

        yield scrapy.Request(commentjsonurl,self.parseComment)

        content = details.xpath("//div[@class='details']//p")

        # download images
        picCount =0
        for c in content:
            if c.xpath("./@align").extract_first()=="center":
                link = c.xpath("./a")
                href = link.xpath("./@href").extract()
                if len(href)<1:
                    continue
                # print(href)
                if "pay" in href[0]:
                    print("pay")
                    continue
                link = link.xpath("./img/@src").extract_first()
                if link is not None:
                    link = "https:"+link
                    # Create folder for each document
                    fileHelper.mkdir(id)
                    # print(link)
                    urllib.urlretrieve(link,"F:/images/"+id+"/"+str(picCount)+".jpg")
                    picCount+=1
        print("Get pic :"+str(picCount+1))

        file = open("txt/"+id + ".txt", "w")
        file.write("link: "+pageLink+"\n\n")
        file.write("title: "+title+"\n\n")
        file.write("author: "+author+"\n\n")
        file.write("time: "+time+"\n\n")
        file.write("source: "+source+"\n\n")
        file.write("tag:" + marks + "\n\n")

        paras = []
        for text in content:
            if text.xpath("./@align").extract_first() =='center':
                paras.append("\n INSERT_PIC_HERE \n")
                continue
            con = text.xpath(".//text()").extract()
            para = ""
            for c in con:
                c = c.replace(u'\xa0',u'')
                para+=c
            paras.append(para)
        paras[len(paras)-1]=""
        for para in paras:
            file.write(para+"\n")
        file.close()
        print('****************************')

# return allCars