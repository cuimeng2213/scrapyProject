# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import parse
from urllib.request import urlretrieve
from scrapy.pipelines.images import ImagesPipeline
from qiche import settings

class QichePipeline(object):
	def __init__(self):
		self.images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
		if not os.path.exists(self.images_path):
			os.mkdir(self.images_path)

	def process_item(self, item, spider):
		#车系路径
		keywords_path = os.path.join(self.images_path, item["keywords"].split(',')[-1])
		if not os.path.exists(keywords_path):
			os.mkdir(keywords_path)
		#图片分类路径
		categroy_path = os.path.join(keywords_path, item["categroy"])
		if not os.path.exists(categroy_path):
			os.mkdir(categroy_path)

		for img_url in item["image_urls"]:
			#图片链接//car3.autoimg.cn/cardfs/product/g24/M08/CF/1A/t_autohomecar__ChcCL1rDVT-AHpL5AAnaFIuHVvM313.jpg
			img_name = img_url.split("_")[-1]
			if not img_url.startswith("https:"):
				img_url = "https:"+img_url
			urlretrieve(img_url,categroy_path+"/"+img_name)
		return item
class QicheAutoSavePipeline(ImagesPipeline):
	def get_media_requests(self, item, info):
		request_objs = super(QicheAutoSavePipeline,self).get_media_requests(item,info)
		for request in request_objs:
			request.item = item

		return request_objs

	def file_path(self, request, response=None, info=None):
		image_store = settings.IMAGES_STORE
		path = super(QicheAutoSavePipeline, self).file_path(request, response, info)
		keywords_path = os.path.join(image_store, request.item.get("keywords").split(",")[-1] )
		if not os.path.exists(keywords_path):
			os.mkdir(keywords_path)
		categroy = os.path.join(keywords_path, request.item.get("categroy"))
		if not os.path.exists(categroy):
			os.mkdir(categroy)

		img_name = path.replace("full/","")
		img_path = os.path.join(categroy, img_name)
		return img_path

