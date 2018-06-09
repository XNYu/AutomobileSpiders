# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class d1Item(scrapy.Item):
    price_after = scrapy.Field()
    price_trend = scrapy.Field()
    brand = scrapy.Field()
    series = scrapy.Field()
    price  = scrapy.Field()
    score = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    engine_power = scrapy.Field()
    _class = scrapy.Field()
    battery_capacity = scrapy.Field()
    charge_normal = scrapy.Field()
    charge_fast = scrapy.Field()
    appearance = scrapy.Field()
    battery_type = scrapy.Field()
    basic = scrapy.Field()
    safety = scrapy.Field()
    interior = scrapy.Field()
    model = scrapy.Field()



class PicItem(scrapy.Item):
    image_url = scrapy.Field()
    images =   scrapy.Field()
class JDItem(scrapy.Item):
    time = scrapy.Field()
    res = scrapy.Field()
    req = scrapy.Field()
    link = scrapy.Field()
    position = scrapy.Field()
    salary = scrapy.Field()
    place = scrapy.Field()
    experience = scrapy.Field()
    edu = scrapy.Field()

class jobItem(scrapy.Item):
    link = scrapy.Field()
    position = scrapy.Field()
    salary = scrapy.Field()
    place = scrapy.Field()
    experience = scrapy.Field()
    edu = scrapy.Field()
    time = scrapy.Field()


class idItem(scrapy.Item):
    id = scrapy.Field()

class scoreItem(scrapy.Item):
    #来源的WebID，品牌，型号，来源
    #油耗，操控，性价比，动力，配置
    #舒适度，空间，外观，内饰，总分

    web_id = scrapy.Field()
    brand  = scrapy.Field()
    name = scrapy.Field()
    source = scrapy.Field()
    fuel = scrapy.Field()
    control = scrapy.Field()
    costperformance = scrapy.Field()
    power = scrapy.Field()
    config = scrapy.Field()
    comfort = scrapy.Field()
    space = scrapy.Field()
    appearance = scrapy.Field()
    interior = scrapy.Field()
    total = scrapy.Field()
    #印象
    impression = scrapy.Field()
    #维修保养(only 163)
    repair = scrapy.Field()

class priceItem(scrapy.Item):
    #网易唯一ID 品牌 型号 价格 来源
    id = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    source = scrapy.Field()

class CarItem(scrapy.Item):
    # define the fields for your item here like:
    #来源网站ID，品牌，产品唯一ID，产品型号，发动机，年份，价格
    web_id = scrapy.Field()
    brand=scrapy.Field()
    product_id= scrapy.Field()
    product_name = scrapy.Field()
    #新加：一层属性类型
    Basic = scrapy.Field()
    Body = scrapy.Field()
    Engine = scrapy.Field()
    Motor = scrapy.Field()
    Battery = scrapy.Field()
    Drive = scrapy.Field()
    Chassis = scrapy.Field()
    Wheel = scrapy.Field()
    Safety = scrapy.Field()
    Control = scrapy.Field()
    Exterior = scrapy.Field()
    Interior = scrapy.Field()
    Light = scrapy.Field()
    Glass = scrapy.Field()
    AC = scrapy.Field()
    Seat = scrapy.Field()
    Multimedia = scrapy.Field()
    Color = scrapy.Field()
    Others = scrapy.Field()

    link = scrapy.Field()
    engine = scrapy.Field()
    year = scrapy.Field()
    price = scrapy.Field()
    #厂商，车身结构，长宽高(mm)，发动机，变速箱，最高车速(km/h)
    #0-100加速时间(s),油耗(L),整车保养期限,常规保养间隔(KM),动力类型
    manufactor = scrapy.Field()
    carStructure = scrapy.Field()
    size = scrapy.Field()
    gearbox = scrapy.Field()
    maximumSpeed = scrapy.Field()
    accelerationTime = scrapy.Field()
    fuelConsumption = scrapy.Field()
    warranty = scrapy.Field()
    maintenanceInterval = scrapy.Field()
    powerType = scrapy.Field()




