import scrapy
from scrapy.http import HtmlResponse
from Productparser.items import ProductparserItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    url = 'https://leroymerlin.ru'

    def __init__(self, search):
        super(LeroymerlinSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']


    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='bex6mjh_plp s15wh9uj_plp l7pdtbg_plp r1yi03lb_plp sj1tk7s_plp']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        goods_links = response.xpath("//a[@data-qa='product-name']/@href").extract()
        for link in goods_links:
            yield response.follow(f'{self.url + link}', callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=ProductparserItem(), response=response)

        loader.add_xpath('name', "//h1[@itemprop='name']/text()")
        loader.add_xpath('photo', "//img[@alt='image thumb']/@src")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_value('good_link', response.url)

        yield loader.load_item()

        # good_link = response.url
        # name = response.xpath("//h1[@itemprop='name']/text()").extract_first()
        # price_str = response.xpath("//span[@slot='price']/text()").extract_first()
        # photo = response.xpath("//img[@alt='image thumb']/@src").extract()
        # item = ProductparserItem(name=name, good_link=good_link, price_str=price_str, photo=photo)
        # yield item