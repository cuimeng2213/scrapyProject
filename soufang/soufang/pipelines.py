# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
from scrapy.exporters import JsonLinesItemExporter

class SoufangPipeline(object):
    def process_item(self, item, spider):
        return item
class NewHousePipeline(object):
    def __init__(self):
        
        self.newhouse_fp = open("x.json",'wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp, ensure_ascii=False)

    def process_item(self, item, spider):
        self.newhouse_exporter.export_item(item)
        return item

    def close_spider(self, spider):
    	self.newhouse_fp.close()
