# -*- coding: utf-8 -*-

#创建爬虫项目：scrapy startproject 项目名
#创建爬虫类：scrapy genspider 类名  域名（可不填）
#启动爬虫类：scrapy crawl 类名  ----启动此类即可执行此命令
#导出数据：scrapy crawl -o name.json/xml/... ---导出相应文件类型的数据

from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'ctripRestaurant'])

