# -*- coding: utf-8 -*-
import scrapy
from qiche.items import QicheItem
from qiche.items import QicheImageUrlsItem

class QczjSpider(scrapy.Spider):
	name = 'qczj'
	allowed_domains = ['autohome.com.cn']
	start_urls = ['https://car.autohome.com.cn/pic/series/526.html#pvareaid=3454438','https://car.autohome.com.cn/pic/series/614.html#pvareaid=3454438']

	def parse(self, response):
		print("AAAAAAA: ", response.status)
		keywords = response.xpath("//meta[@name='keywords']/@content").get()
		print("AAAAAAAAAAAAAA: ", keywords)

		categroys = response.xpath("//div[@class='uibox']")[1:]
		
		for categroy in categroys:
			item = QicheImageUrlsItem()
			cate = categroy.xpath("./div[1]/a[1]/text()").get()
			#print("categroy is : ", cate)
			image_urls = categroy.xpath(".//img/@src").getall()
			image_urls = list( map(lambda url: "https:"+url.replace("t_","1024x0_1_q87_"), image_urls) )
			#print("DDDDDDDDDDDDD: ", type(image_urls), image_urls)
			item["categroy"] = cate
			item["image_urls"] = image_urls
			item["keywords"] = keywords
			yield item
