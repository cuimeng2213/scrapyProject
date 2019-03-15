# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewHouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    #几居室有可能是一个列表
    rooms = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    #行政区
    district = scrapy.Field()
    #是否在售
    sale = scrapy.Field()
    #详情页面url
    origin_url = scrapy.Field()
    house_style =scrapy.Field()
    
class ESFHouseItem(scrapy.Item):
    province_name = scrapy.Field()
    city =scrapy.Field()
    name =scrapy.Field()
    price =scrapy.Field()
    rooms =scrapy.Field()
    floor =scrapy.Field()
    origin_url =scrapy.Field()
    area = scrapy.Field()
    toward = scrapy.Field()
    unit_price =scrapy.Field()
    year =scrapy.Field()
    contacts =scrapy.Field()
    contacts_url =scrapy.Field()
    house_style =scrapy.Field()

