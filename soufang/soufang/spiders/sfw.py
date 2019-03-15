# -*- coding: utf-8 -*-
import re
import scrapy
from urllib.parse import urljoin
from soufang.items import NewHouseItem


class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['lf.fang.com','hf.newhouse.fang.com','newhouse.fang.com','esf.fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']
    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']/table/tr")[1:]
        for tr in trs:
            tds = tr.xpath("./td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s","", province_text)
            if province_text == "其它":
                continue
            if province_text:
                #print(province_text)
                #保存省份名字，如果为None则使用前一次保存得
                province_name = province_text
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath("./@href").get()
                #print("%s %s" % (province_name, city))
                
                #拼接二手房和新房url

                if "bj." in city_url:
                    continue
                    newhouse_url = "https://newhouse.fang.com/house/s/"
                    esf_url = "https://esf.fang.com/"
                else:
                    #https://hf.newhouse.fang.com/house/s/
                    #http://hf.fang.com/
                    #https://hf.newhouse.fang.com/house/s/
                    #http://hf.fang.com/
                    suoxie = city_url.split('.')[0].split('/')[-1]
                    newhouse_url = "https://{}.newhouse.fang.com/house/s/".format(suoxie)
                    #https://hf.esf.fang.com/
                    esf_url = "https://{}.esf.fang.com/".format(suoxie)
                    
                print(">>>>>>>>>>: %s %s" % (newhouse_url, esf_url))
                yield scrapy.Request(newhouse_url, callback=self.parse_newhouse, meta = {"info":(province_name, city)} )

                yield scrapy.Request(esf_url, callback=self.parse_esf, meta = {"info":(province_name, city)} )
                break
            break
    def parse_newhouse(self, response):
        province_name, city_name = response.meta.get("info")
        print("###############", province_name, city_name)
        lis = response.xpath("//div[@class='nhouse_list']//li")
        print(len(lis))
        for li in lis:
            name = li.xpath(".//div[contains(@class,'house_value')]/div[@class='nlcd_name']/a/text()").get()
            if name:
                name = name.strip()
            #print(name)
            house_type = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
            #print(house_type)
            area = li.xpath(".//div[contains(@class,'house_type')]//text()").getall()
            if area:
                area = re.sub(r"\s|－","", area[-1])
            relative_message = li.xpath(".//div[contains(@class,'relative_message')]/div[@class='address']/a/@title").get()
            if relative_message:
                address = relative_message
                district = re.search(r".*\[(.*)\].*", relative_message).group(1)
            sale = li.xpath("//div[contains(@class,'fangyuan')]/span[@class='inSale']/text()").get()
            if sale:
                sale = sale
            origin_url = li.xpath(".//div[contains(@class,'house_value')]/div[@class='nlcd_name']/a/@href").get()
            if origin_url:
                origin_url=response.urljoin(origin_url)

            price = li.xpath(".//div[@class='nhouse_price']//text()").getall()
            if price:
                price = re.sub(r"\s","", "".join(price))
            item = NewHouseItem(province= province_name, city=city_name, name=name,price=price,sale=sale,origin_url=origin_url,rooms=house_type,area=area,district=district)
            yield item
            
        #当请求到第6页页面上有两个符合匹配规则的下一页地址，此处使用最后一个
        #next_page = response.xpath("//a[@class='next']/@href").getall()
        #if next_page:
            #print("###################: netx_page: ", next_page)
            #yield scrapy.Request(urljoin(response.url, next_page[-1]), callback = self.parse_newhouse)



    '''
    def parse(self, response):
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

                item = {"province_name":province_name,"city_name":name}

                yield scrapy.Request(newhouse_url, callback=self.parse_newhouse, meta = item)

                yield scrapy.Request(esf_url, callback=self.parse_esf)
                break
            break
    '''
    '''
    def strip_list_space(self, l):
        return l and l.strip()
            
    def parse_newhouse(self, response):
        province_name, city = response.meta.get("info")
        houses = response.xpath("//div[@class='nl_con clearfix']/ul/li") 
        for house in houses:
            item = NewHouseItem()
            name = house.xpath(".//div[@class='nlc_details']/div[contains(@class,'house_value')]/div[@class='nlcd_name']/a/text()").get()
            if name:
                name = name.strip()
                item["name"] = name
            position = house.xpath(".//div[@class='nlc_details']/div[contains(@class,'relative_message')]/div[@class='address']/a/@title").get()
            if position:
                position = position.strip()
                item["position"] = position
            resource = house.xpath(".//div[@class='nlc_details']/div[contains(@class,'fangyuan')]//text()").getall()
            if resource:
                resource = list( filter(self.strip_list_space, resource) )
                item["resource"] = resource
            house_type = house.xpath(".//div[@class='nlc_details']/div[contains(@class,'house_type')]//text()").getall()
            if house_type:
                house_type = re.sub( r"\s","","".join(house_type) ).split("－")
                print(house_type)
                if len(house_type)>=2:
                    item["house_type"] = house_type[0]
                    item["house_area"] = house_type[1]
                else:
                    item["house_type"] = house_type[0]

            house_price = house.xpath(".//div[@class='nlc_details']/div[contains(@class,'nhouse_price')]//text()").getall()
            if house_price:
                house_price = re.sub(r"\s","","".join(house_price)) 
                item["house_price"] = house_price
            yield item
        #当请求到第6页页面上有两个符合匹配规则的下一页地址，此处使用最后一个
        next_page = response.xpath("//a[@class='next']/@href").getall()
        if next_page:
            print("###################: netx_page: ", next_page)
            yield scrapy.Request(urljoin(response.url, next_page[-1]), callback = self.parse_newhouse)
    '''
    def parse_esf(self, response):
        #print(">>>>>>>>>>>>>>: ", response.status)
        pass
