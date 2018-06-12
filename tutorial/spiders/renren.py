#coding=utf-8
import scrapy
import sys
import xlrd
import xlutils
import xlwt
from xlutils.copy import copy
import tutorial.Helper.stringHelper as strHelper
from tutorial import items

reload(sys)
sys.setdefaultencoding('utf-8')

class LiepinSpider(scrapy.Spider):
    name = "rrc"
    tlts = []
    def start_requests(self):
        file = open("inputs/rrc_titles.txt","r")
        for t in file.readlines():
            self.tlts.append(strHelper.format(t))
        file.close()

        file = open("inputs/rrclinks.txt","r")
        for link in file.readlines():
            if "http" not in link:
                continue
            base_url = strHelper.format(link)
            request = scrapy.Request(
                base_url,
                callback=self.parseCars,
                dont_filter=True)
            yield request

    def parseCars(self,response):
        cars = response.xpath("//ul[@class='row-fluid list-row js-car-list']//a/@href").extract()
        results = response.xpath("//p[@class='result']//text()").extract()
        res = ""
        for r in results:
            res+=r
        file = open("inputs/car_count_rrc.txt","w")
        file.write(res)
        file.close()
        # print(len(cars))
        base_url = 'https://www.renrenche.com'
        for car in cars:
            car = base_url+car
            yield scrapy.Request(car,self.parse)
        nextPage = response.xpath("//div[@class='container text-center search-pagination-wrapper']//a/@href").extract()
        nextPage =base_url+ nextPage[len(nextPage)-1]
        if "java" not in nextPage:
            yield scrapy.Request(nextPage,self.parseCars)

    def parse(self,response):
        print(response.url)
        tt = self.tlts
        dict = {}
        bb = response.xpath("//p[@class='detail-breadcrumb-tagP']/a/text()").extract()
        # 品牌，型号，名称
        dict[tt[0]] = strHelper.numberTrans(bb[2])
        dict[tt[1]] = strHelper.numberTrans(bb[3])
        dict[tt[2]] = strHelper.numberTrans(bb[4])
        price = response.xpath("//p[@class='price detail-title-right-tagP']/text()").extract_first()
        price = price[1:len(price)]
        dict[tt[3]] = price
        bbbbasicAttr = response.xpath("//div[@class='row-fluid-wrapper']//li//strong/text()")
        license_city = response.xpath("//div[@class='row-fluid-wrapper']//li//strong[@id]/@licensed-city").extract_first()
        # print(license_city)
        basicAttr = []
        for t in bbbbasicAttr:
            t= t.extract()
            basicAttr.append(strHelper.numberTrans(t))
        basicAttr.append(license_city)
        for i in range(0,len(basicAttr)):
            dict[tt[i+4]] = basicAttr[i]

        extendedAttrs = response.xpath("//div[@id='js-parms-table']//table")
        for table in extendedAttrs:
            trs = response.xpath(".//tr")
            trs = trs[1:len(trs)]
            for tr in trs:
                tds = tr.xpath(".//td")
                for td in tds:
                    title = td.xpath("./div[@class='item-name']/text()").extract_first()
                    title = strHelper.format(title)
                    title = title.encode("utf-8")
                    value = td.xpath("./div[@class='item-value']/text()").extract_first()
                    value = strHelper.format(value)
                    value = value.encode("utf-8")
                    dict[title] = value
        keys = dict.keys()
        for title in tt:
            if title not in keys:
                dict[title] = "无".encode("utf-8")

        rexcel = xlrd.open_workbook("inputs/ershou.xls")
        row_count = rexcel.sheets()[0].nrows
        excel = copy(rexcel)
        sheet = excel.get_sheet(0)

        # for i in range(0,len(tt)):
        #     sheet.write(0, i, tt[i])
        for i in range(0,len(tt)):
            sheet.write(row_count,i,dict[tt[i]])
        i+=1
        sheet.write(row_count,i,response.url)
        excel.save("inputs/ershou.xls")

        #
        # titles=[]
        # titles.append("品牌".decode())
        # titles.append("型号".decode())
        # titles.append("名称".decode())
        # titles.append("报价".decode())
        #
        # basicAttrs = response.xpath("//div[@class='row-fluid-wrapper']//p[@class='small-title']/text()").extract()
        # for t in basicAttrs:
        #     titles.append(strHelper.format(t))
        #
        # extendedAttrs = response.xpath("//div[@id='js-parms-table']//table//div[@class='item-name']/text()").extract()
        # for t in extendedAttrs:
        #     titles.append(strHelper.format(t))
        # file = open("inputs/rrc_titles.txt","w")
        # for t in titles:
        #     file.write(t+"\n")
        # file.close()


# return allCars