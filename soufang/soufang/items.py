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
    name = scrapy.Field()
    position = scrapy.Field()
    resource = scrapy.Field()
    house_type = scrapy.Field()
    house_area = scrapy.Field()
    house_price = scrapy.Field()
