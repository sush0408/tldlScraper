# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class TarladalalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Ingredient(Item):
    name = Field()
    quantity = Field()
    unit = Field()
    properties= Field()


class Recipe(Item):
    id = Field()
    name = Field()
    author = Field()
    description = Field()
    ingredients = Field()
    instructions = Field()
    image_link = Field()
    image_main = Field()
    images_instruction = Field()
    category = Field()
    prep_time = Field()
    cook_time = Field()
    published_date = Field()
    updated_date = Field()
    url=Field()
    tags= Field()
    accompaniments = Field()
