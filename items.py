# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def photo_to_big(value):
    try:
        result = value.replace('w_82,h_82', 'w_500,h_500')
        return result
    except Exception:
        return value

def price_to_int(value):
    price = int(value.replace(' ', ''))
    return price

class ProductparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    good_link = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(price_to_int))
    photo = scrapy.Field(input_processor=MapCompose(photo_to_big))
    pass
