import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import LabirintItem

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/Python/?stype=0']


    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@title='Следующая']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-title-link']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.book_parse)


    def book_parse(self, response: HtmlResponse):
        book_link = response.url
        name = response.xpath("//strong[@class='pmb-title']/text()").extract_first().replace('Рецензии на книгу ', '')
        author = response.xpath("//a[@data-event-label='author']/text()").extract_first()
        old_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        new_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        rating = response.xpath("//div[@id='rate']/text()").extract_first()

        item = LabirintItem(name=name, author=author, old_price=old_price, new_price=new_price, rating=rating, book_link=book_link)
        yield item