#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 18:26:54 2020

@author: niccolodiana
"""

#Here from all the pages of all subcategories I am gettin the link of every product in that page
import scrapy

class MySpider(scrapy.spiders.Spider):
    name = 'carrefour'

    with open('MultiplePagesPerSubcategory.txt','r') as f:
        endurls = f.read()
        f.close()
    
    endurls= endurls.split(sep=' ')
    #endurls = ['https://www.carrefour.es'+url for url in endurls]
        
    start_urls = endurls
    
    def parse(self, response):
        
        pages_in_category = response.xpath("//div[@class='brand']/a/@href").getall()
        #length = len(pages_in_category)
        pages_in_category = ['https://www.carrefour.es'+page for page in pages_in_category]
        with open('SingleProductsList.txt', 'a') as f:
            for page in pages_in_category:
                f.write(page)
                f.write(' ')