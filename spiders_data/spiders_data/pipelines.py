# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pyArango.connection import *
import time

class SpidersDataPipeline(object):
    def __init__(self):
        self.conn = Connection(username='ybbapp', password='se4dr5ft6', arangoURL='http://172.26.30.57:8529')
        self.db = self.conn['ybbapp']

    def process_item(self, item, spider):
        scrapy_data = self.db['spiders_ctrip_data']
        doc = scrapy_data.createDocument()
        doc['data'] = item
        doc['createdTime'] = int(round(time.time() * 1000)) #毫秒级时间戳
        doc.save()