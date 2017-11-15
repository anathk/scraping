# -*- coding: utf-8 -*-
#from __future__ import absolute_import
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime
import time
import sys
from pprint import pprint
import csv

sys.path.append('/home/zchao/github/scraping/apkcrawler')
from apkcrawler.items import ApkcrawlerItem


class ApkpureSpider(scrapy.Spider):
    name = 'apkpure'
    allowed_domains = ['apkpure.com']
    start_urls = ['https://apkpure.com/game']
    
    #csvwriter = csv.writer(open('apk_items.csv', 'w+'))
    
    #rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(LinkExtractor(allow=('/beauty', ), deny=('/game_[a-z_]+', )), callback='testparse', follow=True),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        #Rule(LinkExtractor(allow=('.*', )), callback='parse', follow=True),)

    def parse(self, response):
        #/html/body/div[2]/div[2]/div/div[2]/div[2]/ul/li[6]/a   apps category
        #/html/body/div[2]/div[2]/div/div[2]/div[2]/ul/li[1]/a   apps category
        
        #/html/body/div[2]/div[2]/div/div[2]/div[1]/ul/li[1]/a   games category
        #/html/body/div[2]/div[2]/div/div[2]/div[1]/ul/li[2]/a   games category
        
        categories = response.xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/ul/li/a').xpath('@href').extract()        
        if categories is not None:
            self.logger.info('-------------------------------------------------------------')
            self.logger.info('Parsing ' + response.url)
            self.logger.info('headers ' + str(response.headers))
            for category in categories:
                for i in range(30):                    
                    category_page = response.urljoin(category + '?page=' + str(i))               
                    yield scrapy.Request(category_page, callback=self.parse_category, meta={'category': category.replace('/', '')})  
                    #yield response.follow(category, callback=self.parse_category, meta={'category': category.replace('/', '')})
        
        
    def parse_category(self, response):
        #//*[@id="pagedata"]/li[1]/div[4]/a Download APK link
        #//*[@id="pagedata"]/li[2]/div[4]/a
        
        #/html/body/div[2]/div[1]/a next page
        
        # //*[@id="pagedata"]/li[2]/div[3]/span average rating

        self.logger.info('========================================================')
        self.logger.info('category Parsing ' + response.url)
        self.logger.info('headers ' + str(response.headers))
        next_page = response.xpath('/html/body/div[2]/div[1]/a').xpath('@href').extract_first()
        download_links = response.xpath('//*[@id="pagedata"]/li/div[4]/a').xpath('@href').extract()
        average_rating = response.xpath('//*[@id="pagedata"]/li[2]/div[3]/span/@title').extract_first()
        try:
            average_rating = average_rating.split()[-1]
        except Exception as e:
            self.logger.info(e.message)
            average_rating = '-1'
           
        # add average_rating to meta.
        response.meta['average_rating'] = average_rating
        
        if download_links is not None:
            for download_link in download_links:
                yield response.follow(download_link, callback=self.parse_download_link, meta=response.meta)
        
        #if next_page is not None:
            #yield response.follow(download_link, callback=self.parse_category)
                
    def parse_download_link(self, response):
        self.logger.info('***********************************************************')
        self.logger.info('download link Parsing ', response.url)
        self.logger.info('headers ' + str(response.headers))
        
        apk_link = response.xpath('//*[@id="download_link"]').xpath('@href').extract_first()
        category = response.meta['category']
        average_rating = response.meta['average_rating']
        self.logger.info('apk_link: ' + apk_link)
        apk_name = response.xpath('/html/body/div[2]/div[1]/div[2]/div[2]/h1/span[2]/text()').extract_first()
        #yield response.follow(apk_link, callback=self.parse_apk)
        yield scrapy.Request(apk_link, meta = {'dont_redirect': True, 
                                               'handle_httpstatus_list': [302], 
                                               'apk_name': apk_name,
                                               'category': category,
                                               'average_rating': average_rating
                                              }, 
                             callback=self.parse_apk)  

    def parse_apk(self, response):
        self.logger.info('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        self.logger.info('download link Parsing ', response.url)
        self.logger.info('headers ' + str(response.headers))
        apk_name = response.meta['apk_name']
        file_urls = response.headers['Location'].decode('utf-8')
        category = response.meta['category']
        average_rating = response.meta['average_rating']
        
        item = ApkcrawlerItem()
        
        
        
        try:
            item['category'] = category
            item['apk_name'] = apk_name
            item['file_urls'] = [file_urls]
            item['average_rating'] = average_rating
            item['crawl_time'] = str(datetime.now())


            self.logger.info('file_urls: ' + file_urls)
            self.logger.info('apk_name: ' + apk_name)
            self.logger.info('category: ' + category)
            self.logger.info('average_rating: ' + average_rating)
        except Exception as e:
            print('2017error')
            print(e)
            
        
        category = item['category']
        apk_name = item['apk_name']
        file_url = item['file_urls'][0]
        average_rating = item['average_rating']
        crawl_time = item['crawl_time']
                    
        with open('apk_items.txt', 'a+') as f:
            f.write('{},{},{},{},{}\n'.format(category, apk_name, file_url, average_rating, crawl_time))
            
        yield item
             


# response.headers.getlist("Set-Cookie")
if __name__=='__main__':  
    #pprint(sys.path)
    #sys.exit()
    print('Start crawling process...')
    start_time = time.time()
    process = CrawlerProcess(get_project_settings())

    process.crawl(ApkpureSpider)
    process.start() # the script will block here until the crawling is finished
    end_time = time.time()
    process_time = int(end_time - start_time)
    print('Crawling process finished in {} seconds.'.format(process_time))
    

