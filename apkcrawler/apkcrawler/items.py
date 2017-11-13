# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ApkcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    apk_name = scrapy.Field()
    file_urls = scrapy.Field()
    average_rating = scrapy.Field()
    crawl_time = scrapy.Field()
    
