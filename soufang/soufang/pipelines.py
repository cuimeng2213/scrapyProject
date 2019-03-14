# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json

class SoufangPipeline(object):
    def process_item(self, item, spider):
        return item
class NewHousePipeline(object):
    def __init__(self):
        self.base_dir = os.path()
        self.fp = open("x.json")
    def process_item(self, item, spider):
        
        return item
