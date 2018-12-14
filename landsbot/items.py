# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class LandsbotItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ts = Field()
    sale_type = Field()
    building_type = Field()
    building_name = Field()
    area = Field()
    supply_area = Field()
    exclusive_area = Field()
    floor = Field()
    sale_floor = Field()
    max_floor = Field()
    sale_price = Field()
    deposit = Field()
    rent_fee = Field()
