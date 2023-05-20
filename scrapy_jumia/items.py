# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose,TakeFirst
from w3lib.html import remove_tags




def process_price(value):
    print('gert',value)
    valu=value.split('₦')[-1].strip().replace(",",'')
    valu =float(valu)
    return valu

def process_kongaprice(value):
    print('gert',value)
    val =value.split('₦')[-1].strip()
    print('gert2',val)
    valu =float(val)
    return valu


def process_url(val):
    value =f'https://www.jumia.com.ng{val}'
    return value

def process_kongaurl(val):
    value =f'https://www.konga.com{val}'
    return value

def process_category(val):
    value=val[-2]
    return value

def process_discount(val):
    return int(val.split('%')[0])


def remove_new_line(value):
    return value.replace('\"','')

class JumiaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=MapCompose(remove_tags,remove_new_line), output_processor=(TakeFirst()))
    original_price =scrapy.Field(input_processor=MapCompose(remove_tags, process_price),output_processor=(TakeFirst()))
    discount_price =scrapy.Field(input_processor=MapCompose(remove_tags, process_price),output_processor=(TakeFirst()))
    stock = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=(TakeFirst()))
    category =scrapy.Field(input_processor=MapCompose(remove_tags,), output_processor=(TakeFirst()))
    store=scrapy.Field(input_processor=MapCompose(remove_tags,), output_processor=(TakeFirst()))
    image=scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=(TakeFirst()))
    url=scrapy.Field(input_processor=MapCompose(process_url),output_processor=(TakeFirst()))
    discount_percent=scrapy.Field(input_processor=MapCompose(remove_tags,process_discount), output_processor=(TakeFirst()))


class KongaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=MapCompose(remove_tags,remove_new_line), output_processor=(TakeFirst()))
    original_price =scrapy.Field(input_processor=MapCompose(remove_tags,process_kongaprice),output_processor=(TakeFirst()))
    discount_price =scrapy.Field(input_processor=MapCompose(remove_tags,process_kongaprice ),output_processor=(TakeFirst()))
    category =scrapy.Field(input_processor=MapCompose(remove_tags,), output_processor=(TakeFirst()))
    store=scrapy.Field(input_processor=MapCompose(remove_tags,), output_processor=(TakeFirst()))
    image=scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=(TakeFirst()))
    url=scrapy.Field(input_processor=MapCompose(process_kongaurl),output_processor=(TakeFirst()))
    dicount_percent=scrapy.Field(input_processor=MapCompose(remove_tags,process_discount), output_processor=(TakeFirst()))

   
