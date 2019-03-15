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
        
        self.newhouse_fp = open("newhouse.json",'wb')
        self.esf_fp = open("esf.json",'wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp, ensure_ascii=False)
        self.esf_exporter = JsonLinesItemExporter(self.esf_fp, ensure_ascii=False)

    def process_item(self, item, spider):
        if "newhouse" == item.get("house_style"):
            self.newhouse_exporter.export_item(item)
        elif "esf" == item.get("house_style"):
            self.esf_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.newhouse_fp.close()
        self.esf_fp.close()

