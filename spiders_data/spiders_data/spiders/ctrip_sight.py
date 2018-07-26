# -*- coding: utf-8 -*-
import scrapy
import re
import logging

from spiders_data.items import CtripSightItem
class CtripSightSpider(scrapy.Spider):
    name = 'ctripSight'
    baseUrl = 'http://you.ctrip.com'
    allowed_domains = ['ctrip.com']
    #start_urls = ['http://you.ctrip.com/sight/taipeicity360.html']
    start_urls = ['http://you.ctrip.com/sight/shanghai2.html']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        url = response.url
        logging.info('Strip sigth city url: %s', url)
        for sel in response.css('.list_wide_mod2 .list_mod2 .rdetailbox'):
            url = self.baseUrl + sel.xpath('.//a/@href').extract_first()
            yield scrapy.Request(url, callback=self.sight_detail)
        last_page = response.css('.ttd_pager.cf .numpage::text').extract_first().strip()
        current_page = response.css('.ttd_pager.cf a.current::text').extract_first().strip()
        if last_page != current_page:
            next_page = response.css('a.nextpage::attr(href)').extract_first()
            next_page_url = self.baseUrl + next_page
            yield scrapy.Request(next_page_url, callback=self.parse)

    def sight_detail(self, response):
         url = response.url
         logging.info('Ctrip sight detail url:  %s', url)
         name = response.css('.detail_tt .f_left')[0].xpath('.//a/text()').extract_first().strip()
         nameEn = response.css('.detail_tt .f_left')[0].xpath('.//p/text()').extract_first().strip()
         logging.info('name: %s, nameEn: %s', name, nameEn)
         description = ''
         for sel in response.css('.detailbox_dashed'):
            dr = re.compile(r'<[^>]+>', re.S)
            header = sel.css('h2').extract_first()
            header = dr.sub('', header).strip()
            content = sel.css('.toggle_l').extract_first()
            content = dr.sub('\n', content).strip()
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
         ctripSightItem['category'] = 'sight'
         ctripSightItem['url'] = url
         ctripSightItem['name'] = name
         ctripSightItem['nameEn'] = nameEn
         ctripSightItem['destination'] = destination
         ctripSightItem['description'] = description
         yield {
             "category": 'sight',
             "url": url,
             "name": name,
             "nameEn": nameEn,
             "destination": destination,
             "description": description
         }






