import scrapy

class UserAgentDemoSpider(scrapy.Spider):
	name = 'uaDemo'
	allowed_domains = ["httpbin.org"]
	start_urls = ["http://httpbin.org/user-agent"]

	def parse(self, response):
		print('header= ', response.headers)

		print(response.text)

		yield scrapy.Request(self.start_urls[0], dont_filter=True)
