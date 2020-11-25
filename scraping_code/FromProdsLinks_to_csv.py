#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 18:33:31 2020

@author: niccolodiana
"""

import scrapy 

class MySpider(scrapy.spiders.Spider):
    name = 'carrefour'
    with open('SingleProductsList.txt', 'r') as f:
        string = f.read()
        prod_urls = string.split(sep=' ')
    
    start_urls = prod_urls
    
    
    def parse(self, response):
        wrote_headers = False
            
        product_name = response.xpath("//h1[@class='product-header__name']/text()").get()
        try:
            if '\n' in product_name:
                product_name=product_name[5:]
            if '\n' in product_name:
                idx = product_name.find('\n') 
                product_name= product_name[:idx] 
        except:
            return
        #Gets the current path, useful for clustering
        breadcrumbs_list = response.xpath("//ul[@class='breadcrumb__list']/li[@class='breadcrumb__item']/a/@title").getall()
        full_path = '/'.join(breadcrumbs_list)
        
        #Gets different prices types
        buybox_price = response.xpath("//div[@class='buybox__prices']/span[@class='buybox__price']/text()").get()
        #create a function to do this to all prices
        if buybox_price:
            if '\n' in buybox_price:
                buybox_price=buybox_price[5:]
                if '\n' in buybox_price:
                    idx = buybox_price.find('\n') 
                    buybox_price= buybox_price[:idx]
                    buybox_price.replace(' ','')
                    
        buybox_price_strikethrough = response.xpath("//div[@class='buybox__prices']/span[@class='buybox__price-strikethrough']/text()").get()
        if buybox_price_strikethrough:
            if '\n' in buybox_price_strikethrough:
                buybox_price_strikethrough=buybox_price_strikethrough[5:]
                if '\n' in buybox_price_strikethrough:
                    idx = buybox_price_strikethrough.find('\n') 
                    buybox_price_strikethrough= buybox_price_strikethrough[:idx]
                    
        buybox_price_current = response.xpath("//div[@class='buybox__prices']/span[@class='buybox__price--current']/text()").get()
        if buybox_price_current:
            if '\n' in buybox_price_current:
                buybox_price_current=buybox_price_current[5:]
                if '\n' in buybox_price_current:
                    idx = buybox_price_current.find('\n') 
                    buybox_price_current= buybox_price_current[:idx]
        
        #Gets the nutriscore of the product if it exists
        
        nutri_score_url = response.xpath("//div[@class='nutri-score']/img/@src").get()
        if nutri_score_url:
            idx = nutri_score_url.find('LOV-Nutriscore_')
            length = len('LOV-Nutriscore_') 
            nutri_score = nutri_score_url[idx+length]
        else:
            nutri_score = None
        
        #Nutrition level box 
        nutrition_kcal = response.xpath("//div[@class='nutrition-graph__graphic-svg']/@data-cal").get()
        nutrition_fibers = response.xpath("//div[@class='nutrition-graph__graphic-svg']/@data-fi").get()
        nutrition_fats = response.xpath("//div[@class='nutrition-graph__graphic-svg']/@data-fa").get()
        nutrition_carbs = response.xpath("//div[@class='nutrition-graph__graphic-svg']/@data-h").get()
        nutrition_proteins = response.xpath("//div[@class='nutrition-graph__graphic-svg']/@data-p").get()
        nutrition_salt = response.xpath("//div[@class='nutrition-graph__graphic-svg']/@data-s").get()
        
        price_per_unit = response.xpath("//div[@class='buybox__price-per-unit']/span/text()").getall()
        price_per_unit = price_per_unit[len(price_per_unit)-1] if len(price_per_unit) != 0 else 0
        if price_per_unit:
            if '\n' in price_per_unit:
                price_per_unit=price_per_unit[5:]
                if '\n' in price_per_unit:
                    idx = price_per_unit.find('\n') 
                    price_per_unit= price_per_unit[:idx]
        
        
        
        ingredients = response.xpath("//p[@class='nutrition-ingredients__content']/text()").getall()
        ingredients = ','.join(ingredients)
        allergens = response.xpath("//span[@class='nutrition-allergens__contain']/text()").getall()
        allergens = ','.join(allergens)
        output = ';'.join([str(product_name),
                           str(full_path),
                           str(buybox_price),
                           str(price_per_unit),
                           str(buybox_price_strikethrough),
                           str(buybox_price_current),
                           str(nutri_score),
                           str(nutrition_kcal),
                           str(nutrition_fibers),
                           str(nutrition_fats),
                           str(nutrition_carbs),
                           str(nutrition_proteins),
                           str(nutrition_salt),
                           str(ingredients),
                           str(allergens)
                           ])
        with open('BebidasOutput.txt', 'a') as f:
            '''
            if not wrote_headers:
                heads = ';'.join(['product_name',
                           'full_path',
                           'buybox_price',
                           'price_per_unit',
                           'buybox_price_strikethrough',
                           'buybox_price_current',
                           'nutri_score',
                           'nutrition_kcal',
                           'nutrition_fibers',
                           'nutrition_fats',
                           'nutrition_carbs',
                           'nutrition_proteins',
                           'nutrition_salt',
                           'ingredients',
                           'allergens'
                           ])
                f.write(heads)
                f.write('\n')
                wrote_headers = True'''
                
            f.write(output)
            f.write('\n')
            f.close()
