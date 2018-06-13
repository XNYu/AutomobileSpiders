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
    name = "sina"
    def start_requests(self):

        # url = "https://www.autohome.com.cn/use/201711/909485.html#pvareaid=102624"
        # base_url = "http://auto.sina.com.cn/service/?page="

        # yield scrapy.Request(url,self.parseOnePage)
        # base_url = "http://auto.sina.com.cn/j_kandian.d.html?docid=fyremfz2599182"
        file = open("F:/sinalinks.txt","r")
        for link in file.readlines():
            re = scrapy.Request(
                strHelper.format(link),
                callback=self.parseOnePage,
                dont_filter=True
            )
            yield re

    def parse(self,response):
        articles = response.xpath("//div[@class='content']//a[@class='img fL']/@href").extract()
        divs = response.xpath("//div[@class='s-left fL clearfix']/h3/a/text()").extract()
        for d in divs:
            print(d)
        # for link in articles:
        #     yield scrapy.Request(link,self.parseOnePage)

    def getID(self,str):
        str = str.split(".html")[0]
        str = str.split("/")[5]
        return str

    def parseComment(self,response):
        print(response.url)
        jsonBody = response.body.decode('gbk').encode('utf-8')
        if "comos" in response.url:
            jsonBody = "{"+jsonBody.split("={")[1]
        else:
            jsonBody = jsonBody.split("(")[1].split(")")[0]
        jsonBody = json.loads(jsonBody)
        comment = jsonBody['result']['count']['total']
        print(comment)
        id = response.url.split("newsid=")[1].split("&group")[0]
        file = open("F:/sina/"+id+".txt","a")
        comment = "Comment:" + str(comment)+"\n"
        file.write(comment)
        file.close()

    def parseOnePage(self, response):
        pictures = []
        meta = response.xpath("//meta[@name='comment']/@content").extract_first()
        id = meta.split("_id:")[1]
        channel = meta.split("channel:")[1]
        channel = channel[0:2]

        details = response.xpath("//div[@class='article clearfix']")
        isA = False
        if "article_" in response.url:
            isA = True
        contents = details.xpath(".//p|.//div")
        fulltext = ""
        for con in contents:
            _class = con.xpath("./@class")
            if len(_class)>0:
                try:
                    if isA:
                        link ="http:"+con.xpath("./img/@src").extract_first()
                    else:
                        link = con.xpath("./img/@src").extract_first()
                    pictures.append(link)
                    fulltext += "INSERT_PIC_HERE\n\n"
                except TypeError:
                    print("")

            else:
                if not isA:
                    if "docid" in response.url:
                        text = con.xpath("./font/text()").extract()
                    else:
                        text = con.xpath("./text()").extract()
                else:
                    text = con.xpath("./font/text()").extract()
                if len(text) >0:
                    text = strHelper.format(text[0])
                    fulltext += text+"\n"

        mark = response.xpath("//div[@class='keywords']/a/text()")
        mark = mark.extract()
        if mark is None:
            mark = []
        marks = ""
        for m in mark:
            marks += m+ ","
        marks = marks[0:len(marks)-1]

        title = details.xpath("//h1/text()").extract_first()
        title = strHelper.format(title)

        tANDs = response.xpath("//div[@class='date-source']")
        time = tANDs.xpath("./span[@class='date']/text()").extract_first()
        time = strHelper.format(time)
        source = tANDs.xpath("./a/text()").extract_first()
        source = strHelper.format(source)
        print(time)
        print(source)

        pageLink = response.url
        commentlink = "http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=" \
                          "{channel}" \
                          "&newsid={id}&group=undefined&compress=0&ie=utf-8&oe" \
                          "=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1&" \
                          "callback=jsonp_1528781515017&_=1528781515017".format(channel=channel,id=id)
        yield scrapy.Request(commentlink, self.parseComment)
        # if "article" in pageLink:
        #     id = pageLink.split("article_")[1].split(".html")[0]
        #     id = id.split("_")
        #     id = id[0]+"-"+id[1]
        #     basecommentlink = "http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=mp&newsid="
        #     end= "&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1&callback=jsonp_1528781515017&_=1528781515017"
        #     commentlink = basecommentlink+id+end
        #     yield scrapy.Request(commentlink, self.parseComment)
        #
        # elif "detail" in pageLink:
        #     id = pageLink.split("detail-i")[1].split(".s")[0]
        #     basecommentlink = "http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=qc&newsid=comos-"
        #     end="&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20&jsvar=loader_1528783247454_78178050"
        #     commentlink = basecommentlink+id+end
        #     yield scrapy.Request(commentlink, self.parseComment)
        # else:
        #     id = pageLink.split("docid=")[1]
        # download images
        picCount =0
        for link in pictures:
            # Create folder for each document
            fileHelper.mkdir(id)
            print(link)
            if link is None:
                continue
            if "http" not in link:
                link = "http:"+link
            urllib.urlretrieve(link,"F:/sina/images/"+id+"/"+str(picCount)+".jpg")
            picCount+=1
        print("Get pic :"+str(picCount+1))
        #
        file = open("F:/sina/"+id + ".txt", "w")
        file.write("link: "+pageLink+"\n\n")
        file.write("title: "+title+"\n\n")
        file.write("time: "+time+"\n\n")
        file.write("source: "+source+"\n\n")
        file.write("tag:" + marks + "\n\n")
        file.write(fulltext+"\n")
        file.close()
        print('****************************')

# return allCars