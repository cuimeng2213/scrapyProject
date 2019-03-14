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
    
