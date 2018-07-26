# -*- coding: utf-8 -*-
import scrapy
import re
import logging

from spiders_data.items import CtripSightItem
class CtripRestaurantSpider(scrapy.Spider):
    name = 'ctripRestaurant'
    baseUrl = 'http://you.ctrip.com'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://you.ctrip.com/restaurant/shanghai2.html']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        logging.info('Ctrip restaurant city url: %s', response.url)
        url = self.baseUrl + response.css('.normalbox .normaltitle')[1].xpath('.//a/@href').extract_first().strip()
        yield scrapy.Request(url, self.more_food)

    def more_food(self, response):
        url = self.baseUrl + response.css('.des_wide .normalbox .n_tabtitle')[0].xpath('.//a/@href').extract_first().strip()
        yield scrapy.Request(url, self.restaurant_item)

    def restaurant_item(self, response):
        for sel in response.css('.list_wide_mod2 .list_mod2 .rdetailbox'):
            url = self.baseUrl + sel.xpath('.//a/@href').extract_first()
            yield scrapy.Request(url, callback=self.restaurant_detail)
        last_page = response.css('.ttd_pager.cf .numpage::text').extract_first().strip()
        current_page = response.css('.ttd_pager.cf a.current::text').extract_first().strip()
        logging.info(last_page)
        logging.info(current_page)
        if last_page != current_page:
            next_page = response.css('a.nextpage::attr(href)').extract_first()
            next_page_url = self.baseUrl + next_page
            yield scrapy.Request(next_page_url, callback=self.restaurant_item)

    def restaurant_detail(self, response):
         url = response.url
         logging.info('Ctrip restaurant detail url:  %s', url)
         name = response.css('.detail_tt .f_left')[0].xpath('.//h1/text()').extract_first().strip()
         nameEn = response.css('.detail_tt .f_left')[0].xpath('.//p/text()').extract_first().strip()
         logging.info('name: %s, nameEn: %s', name, nameEn)
         dr = re.compile(r'<[^>]+>', re.S)
         description = response.css('.detailcon')[0].extract()
         description = dr.sub('', description).replace('\r\n', '').strip()
         logging.debug('description: %s', description)
         destination = ''
         for sel in response.xpath('//div[@class="breadbar_v1 cf"]/ul[1]/li')[2:]:
            result = sel.xpath('a/text()').extract()
            if len(result) != 0:
                destination += result[0] + u'-'
         if len(destination) != 0:
            destination = destination[:len(destination) - 1]
         logging.info('destination: %s', destination)

         ctripSightItem = CtripSightItem()
         ctripSightItem['category'] = 'restaurant'
         ctripSightItem['url'] = url
         ctripSightItem['name'] = name
         ctripSightItem['nameEn'] = nameEn
         ctripSightItem['destination'] = destination
         ctripSightItem['description'] = description
         yield {
             "category": 'restaurant',
             "url": url,
             "name": name,
             "nameEn": nameEn,
             "destination": destination,
             "description": description
         }






