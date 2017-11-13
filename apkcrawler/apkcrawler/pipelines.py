# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class ApkcrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
    
    
class CsvWriterPipeline(object):

    def __init__(self):
        self.csvwriter = csv.writer(open('apk_items.csv', 'w'))

    def process_item(self, item, spider):
        
        try:
            category = item['category']
            apk_name = item['apk_name']
            file_url = item['file_urls'][0]
            average_rating = item['average_rating']
            crawl_time = item['crawl_time']
            
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print('Write csv:')
            
            print('file_urls: ' + file_url)
            print('apk_name: ' + apk_name)
            print('category: ' + category)
            print('average_rating: ' + average_rating)
            print('crawl_time: ' + crawl_time)
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')


            self.csvwriter.writerow('{},{},{},{},{}'.format(category, apk_name, file_url, average_rating, crawl_time))
        except Exception as e:
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print(e)
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            
        return item