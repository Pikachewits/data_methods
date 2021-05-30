import scrapy


class LabirintItem(scrapy.Item):
    book_link = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    old_price = scrapy.Field()
    new_price = scrapy.Field()
    rating = scrapy.Field()
    _id = scrapy.Field()

class Book24Item(scrapy.Item):
    book_link = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    old_price = scrapy.Field()
    new_price = scrapy.Field()
    rating = scrapy.Field()
    _id = scrapy.Field()