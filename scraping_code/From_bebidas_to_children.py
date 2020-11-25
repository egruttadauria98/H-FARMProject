#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 17:56:12 2020

@author: niccolodiana
"""
import scrapy

class MySpider(scrapy.spiders.Spider):
    name = 'carrefour'
    '''
    with open('resultt.txt','r') as f:
        endurls = f.read()
        f.close()'''
    
    #endurls= endurls.split(sep=' ')
    #endurls = ['https://www.carrefour.es'+url for url in endurls]
        
    start_urls = ['https://www.carrefour.es/supermercado/bebidas/N-rkxfmc/c']
    
    def parse(self, response):
        
        pages_in_category = response.xpath("//div[@class='category']/a/@href").getall()
        #length = len(pages_in_category)
        pages_in_category = ['https://www.carrefour.es'+page for page in pages_in_category]
        with open('BebidasCategoriesLinks.txt', 'a') as f:
            for page in pages_in_category:
                f.write(page)
                f.write(' ')
                        
'''
       
    def parse_single_products_page(self, response):
        self.logger.info('Visited %s', response.url)
        with open('allinks.txt','a') as f:
            for entry in response.xpath("//article[@class='product-card-item']"):
                res = entry.xpath("./div[@class='text']/div[@class='brand']/a/@href").getall().default('None')
                for i in res:
                    f.append(i)
                
                yield(res)'''