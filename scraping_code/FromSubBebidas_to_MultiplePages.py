#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 18:23:25 2020

@author: niccolodiana
"""

import scrapy

class MySpider(scrapy.spiders.Spider):
    name = 'carrefour'
    with open('BebidasSubCategoriesLinks.txt','r') as f:
        endurls = f.read()
        f.close()
    
    endurls= endurls.split(sep=' ')
    #endurls = ['https://www.carrefour.es'+url for url in endurls]
        
    start_urls = endurls
    
    def parse(self, response):
        
        pages_in_category = response.xpath("//select[@class='selectPagination']/option/@value").getall()
        length = len(pages_in_category)
        pages_in_category = ['https://www.carrefour.es'+page for page in pages_in_category]
        with open('MultiplePagesPerSubcategory.txt', 'a') as f:
            if length != 0:
                for page in pages_in_category:
                    f.write(page)
                    f.write(' ')
            else:
                f.write(str(response.url))
                f.write(' ')