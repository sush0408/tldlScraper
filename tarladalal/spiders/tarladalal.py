import os
import re
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.linkextractor import LinkExtractor
from tarladalal.items import Recipe ,Ingredient
import time
import json


class vegRecipeScraper(CrawlSpider):
    # The name of the spider
    name = "tarla"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains=["tarladalal.com"]

    deny_words = ['/recipes/','privacy','terms','media','/recipe/','About','Archives',\
                    'index','comment','email','about']

    # The URLs to start with
    start_urls = ["https://www.tarladalal.com/RecipeCategories.aspx"]

    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                deny = (deny_words),
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_items(self,response):
        time.sleep(2)

        if response.xpath('//div[@id="rcpinglist"]'):
        
            recipe = Recipe()
            # id
            recipe['id'] = response.url.split('/')[3]

            # name
            recipe['name'] = response.xpath('//span[@id="ctl00_cntrightpanel_lblRecipeName"]/text()').extract_first()

            # author
            recipe['author'] = response.xpath('//span[@id="ctl00_cntrightpanel_lblContribby"]/text()').extract_first()

            # description
            recipe['description'] = response.xpath('//span[@id="ctl00_cntrightpanel_lblDesc"]/text()').extract_first()

            # ingredients
            ingredients = []
            ingredient_nodes = response.xpath('//div[@id="rcpinglist"]/div/span').extract()
            for i in range(len(ingredient_nodes)):
                try:
                    name = response.xpath('//span[@itemprop="recipeIngredient"]/a/span/text()')[i].extract()
                    quantity = response.xpath('//span[@itemprop="recipeIngredient"]/span/text()')[i].extract()
                    properties = response.xpath('//span[@itemprop="recipeIngredient"]/text()')[i].extract()
                except:
                    continue

                ingredient = Ingredient()
                ingredient['name'] = name
                ingredient['quantity'] = quantity
                ingredient['properties'] = properties
                ingredients.append(ingredient)
            recipe['ingredients'] = ingredients

            # instructions
            recipe['instructions'] = response.xpath('//ol/li/span/text()').extract()

            recipe['image_link'] = "https://www.tarladalal.com/"

            #Image Instruction
            recipe['images_instruction'] = response.xpath('//ol/li/span/img/@src').extract()

            # MAIN IMAGE
            recipe['image_main'] = response.xpath('//img[@id="ctl00_cntrightpanel_imgRecipe"]/@src').extract_first().split('?')[0]

            #TAGS
            recipe['tags'] = response.xpath('//div[@class="tags"]/a/text()').extract()

            recipe['prep_time'] =  response.xpath('//p/time/text()')[0].extract()

            recipe['cook_time'] =  response.xpath('//p/time/text()')[1].extract()

            nav = response.xpath('//span[@class="breadcrumb-link-wrap"]/a/span/text()').extract()

            recipe['category'] = nav[len(nav)-1]

            recipe['url'] = response.url

            print(recipe)

            return recipe