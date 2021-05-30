import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import Book24Item


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=it']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class = 'pagination__item _link _button _next smartLink']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@itemprop='name']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.book_parse)


    def book_parse(self, response: HtmlResponse):
        book_link = response.url
        name = response.xpath("//span[@class='breadcrumbs__link']/text()").extract_first()
        author = response.xpath("//a[@class='item-tab__chars-link']/text()").extract_first()
        old_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        new_price = response.xpath("//b[@itemprop='price']/text()").extract_first()
        rating = response.xpath("//span[@class='rating__rate-value']/text()").extract_first()

        item = Book24Item(name=name, author=author, old_price=old_price, new_price=new_price, rating=rating, book_link=book_link)
        yield item