# -*- coding: utf-8 -*-
import scrapy
import re
import logging

from spiders_data.items import CtripSightItem
class CtripShoppingSpider(scrapy.Spider):
    name = 'ctripShopping'
    baseUrl = 'http://you.ctrip.com'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://you.ctrip.com/shopping/shanghai2.html']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        logging.info('Ctrip shopping city url: %s', response.url)
        url = self.baseUrl + response.css('.normalbox .normaltitle')[1].xpath('.//a/@href').extract_first().strip()
        yield scrapy.Request(url, self.more_goods)

    def more_goods(self, response):
        url = self.baseUrl + response.css('.des_wide .normalbox .n_tabtitle')[0].xpath('.//a/@href').extract_first().strip()
        yield scrapy.Request(url, self.goods_item)

    def goods_item(self, response):
        for sel in response.css('.list_wide_mod2 .list_mod2 .rdetailbox'):
            url = self.baseUrl + sel.xpath('.//a/@href').extract_first()
            yield scrapy.Request(url, callback=self.restaurant_detail)
        last_page = response.css('.ttd_pager.cf .numpage::text').extract_first().strip()
        current_page = response.css('.ttd_pager.cf a.current::text').extract_first().strip()
        logging.info('last_page: %s', last_page)
        logging.info('current_page: %s', current_page)
        if last_page == current_page:
            next_page = response.css('a.nextpage::attr(href)').extract_first()
            next_page_url = self.baseUrl + next_page
            yield scrapy.Request(next_page_url, callback=self.restaurant_item)

    def restaurant_detail(self, response):
         url = response.url
         logging.info('Ctrip goods detail url:  %s', url)
         name = response.css('.detail_tt .f_left')[0].xpath('.//h1/a/text()').extract_first().strip()
         nameEn = response.css('.detail_tt .f_left')[0].xpath('.//p/text()').extract_first().strip()
         logging.info('name: %s, nameEn: %s', name, nameEn)
         dr = re.compile(r'<[^>]+>', re.S)
         description = ''
         for sel in response.css('.detailcon.detailbox_dashed'):
            dr = re.compile(r'<[^>]+>', re.S)
            header = sel.css('h2').extract_first()
            header = dr.sub('', header).strip()
            content = sel.css('.toggle_l .description').extract_first()
            content = dr.sub('  ', content)
            description += header + '\n' + content + '\n'
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
         ctripSightItem['category'] = 'shopping'
         ctripSightItem['url'] = url
         ctripSightItem['name'] = name
         ctripSightItem['nameEn'] = nameEn
         ctripSightItem['destination'] = destination
         ctripSightItem['description'] = description
         yield {
             "category": 'shopping',
             "url": url,
             "name": name,
             "nameEn": nameEn,
             "destination": destination,
             "description": description
         }






