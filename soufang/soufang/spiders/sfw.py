# -*- coding: utf-8 -*-
import re
import scrapy
from urllib.parse import urljoin
from soufang.items import NewHouseItem, ESFHouseItem
from scrapy_redis.spiders import RedisSpider


class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['lf.fang.com','hf.newhouse.fang.com','newhouse.fang.com','esf.fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = "fang:url"
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
                yield scrapy.Request(newhouse_url, callback=self.parse_newhouse_next_page, meta = {"info":(province_name, city)} )

                yield scrapy.Request(esf_url, callback=self.parse_esf_next_page, meta = {"info":(province_name, city)} )
                #break
            #break
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
                district =  re.search(r".*\[(.*)\].*", relative_message)
                if district:
                    district = district.group(1)
            sale = li.xpath("//div[contains(@class,'fangyuan')]/span[@class='inSale']/text()").get()
            if sale:
                sale = sale
            origin_url = li.xpath(".//div[contains(@class,'house_value')]/div[@class='nlcd_name']/a/@href").get()
            if origin_url:
                origin_url=response.urljoin(origin_url)

            price = li.xpath(".//div[@class='nhouse_price']//text()").getall()
            if price:
                price = re.sub(r"\s","", "".join(price))
            item = NewHouseItem(province= province_name, city=city_name, name=name,price=price,sale=sale,origin_url=origin_url,rooms=house_type,area=area,district=district,house_style="newhouse")
            yield item
    def parse_newhouse_next_page(self, response):
        '''
        拼接下一页的请求地址
            url格式为：/house/s/b9{}/
        '''
        province_name, city_name = response.meta.get("info")
        last_page = response.xpath("//a[@class='last']/text()").get()
        if last_page:
            last_page = last_page.strip()
            if last_page != "尾页":
                return
            next_url = response.xpath("//a[@class='last']/@href").get()
            url_count = re.search(r".*b9(\d+).*", next_url)
            if not url_count:
                return
            url_count = int(url_count.group(1)) + 1
            for i in range(1, url_count):
                url = response.urljoin("/house/s/b9{}/".format(i))
                yield scrapy.Request(url=url, callback=self.parse_newhouse, meta={"info":(province_name, city_name)})
    def parse_esf_next_page(self, response):
        province_name, city_name = response.meta.get("info")
        all_page = response.xpath("//div[@class='page_al']/p[last()]/text()").get()
        if all_page:
            count = re.search(r".*共(\d+)页.*", all_page)
            if not count:
                return
            count = int(count.group(1))+1
            for i in range(1,count):
                url = response.urljoin("/house/i3{}/".format(i))
                print("#########: ",url)
                yield scrapy.Request(url = url, callback=self.parse_esf, meta = {"info":(province_name,city_name)})

    def parse_esf(self, response):
        province_name, city_name = response.meta.get("info")
        dls = response.xpath("//div[contains(@class, 'shop_list')]/dl")
        for dl in dls:
            name = dl.xpath(".//p[@class='add_shop']/a/@title").get()
            if name:
                print(name)
            price = dl.xpath(".//dd[@class='price_right']/span[1]//text()").getall()
            if price:
                price = "".join(price)
            unit_price = dl.xpath(".//dd[@class='price_right']/span[2]//text()").get()
            #print(unit_price)
            origin_url = dl.xpath(".//h4[@class='clearfix']/a/@href").get()
            origin_url = response.urljoin(origin_url)
            #print(origin_url)
            house_info = dl.xpath(".//p[@class='tel_shop']//text()").getall()
            try:
                if house_info:
                    house_info = "".join(house_info)
                    house_infos = re.sub(r"\s","", house_info).split("|")[:-1]
                    print(house_infos)
                    toward = ""
                    rooms= ""
                    floor =""
                    year = ""
                    area = ""
                    for info in house_infos:
                        if "厅" in info:
                            rooms = info
                        elif "向" in info:
                            toward = info
                        elif "层" in info:
                            floor = info
                        elif "年" in info:
                            year = info
                        else:
                            area = info
                contacts = dl.xpath(".//p[@class='tel_shop']/span[@class='people_name']/a/text()").get()
                contacts_url = dl.xpath(".//p[@class='tel_shop']/span[@class='people_name']/a/@href").get()
                contacts_url = response.urljoin(contacts_url)
                print(contacts_url)
                item = ESFHouseItem(province_name=province_name, city=city_name, price=price, rooms=rooms,floor=floor,origin_url=origin_url,area=area,toward=toward,unit_price=unit_price,year=year,contacts_url=contacts_url, contacts=contacts, house_style="esf")
                yield item
            except Exception as e:
                print(">>>>>>>>>>>>: ",e)
            
