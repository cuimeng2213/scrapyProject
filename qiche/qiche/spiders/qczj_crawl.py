#coding: utf-8
import scrapy
from qiche.items import QicheImageUrlsItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class Qczj_CrawlSpider(CrawlSpider):
	name = "qczj_crawl"
	start_urls = ["https://www.autohome.com.cn/car/"]

	#https://car.autohome.com.cn/pic/series/614-1.html#pvareaid=2042222
	#https://car.autohome.com.cn/pic/series/614-10-p2.html#pvareaid=2042222
	#follow=True 爬去打开页面中与Rule匹配的页面
	rules = ( Rule( LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/\d+?\.html') , callback="print_car_name", follow=True)
			  ,Rule( LinkExtractor(allow=r'(https://www.autohome.com.cn/\d+?/)#levelsource') , callback="print_car_name", follow=True)
			  ,Rule( LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/\d+-\d+.*?\.html') , callback="parse_items", follow=True) )

	def parse_items(self, response):
		keywords = response.xpath("//div[@class='cartab-title']/h2/a/text()").get()
		categroy = response.xpath("//div[@class='uibox']/div/text()").get()
		image_urls = response.xpath("//div[@class='uibox-con carpic-list03 border-b-solid']//img/@src").getall()
		#给图片url添加https协议头，并且替换t_字符串为1024x0_1_q87_后下载高清图片
		image_urls = list( map(lambda url: "https:"+url.replace("t_","1024x0_1_q87_"), image_urls) )
		item = QicheImageUrlsItem()
		item["image_urls"] = image_urls
		item["keywords"] = keywords
		item["categroy"] = categroy
		print("车系列: %s 图片分类: %s" % (keywords, categroy))
		#yield item

	def print_car_name(self, response):
		car_name = response.xpath("//meta[@name='keywords']/@content").get().split(",")[-1]
		print("car_name: %s" % car_name)
