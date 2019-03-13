# -*- coding: utf-8 -*-
import scrapy


class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['lf.fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        print("aaaaaaa: ", response.status)
        provinces = response.xpath("//div[@class='outCont']/table/tr")[1:]
        for province in provinces:
            tds = province.xpath("./td")
            province_name = tds[1].xpath(".//text()").get().strip()
            if province_name == "其它":
                continue
            if province_name:
                print(province_name)
            citys = tds[2].xpath("./a")
            for city in citys:
                name = city.xpath("./text()").get().strip()
                url = city.xpath("./@href").get().strip()
                #print("name: %s url: %s" % (name, url))
                #https://hf.newhouse.fang.com/house/s/
                #http://hf.fang.com/
                suoxie = url.split('.')[0].split('/')[-1]
                newhouse_url = "https://{}.newhouse.fang.com/house/s/".format(suoxie)
                print("newhouse_url: ", newhouse_url)
                #https://hf.esf.fang.com/
                esf_url = "https://{}.esf.fang.com/".format(suoxie)




