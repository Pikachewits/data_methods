from pymongo import MongoClient
from lxml import html
import requests
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['lenta_news']
collections = db.lenta_collection


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

response = requests.get('https://lenta.ru/')
dom = html.fromstring(response.text)


items = dom.xpath("//div[@class = 'span4']/div[@class = 'item' or @class = 'first-item']")

for item in items:
    news ={}
    news['resource'] = "lenta.ru"
    name_path = item.xpath(".//a[contains (@href, '/news/')]/text()")[0].replace('\xa0', ' ')
    news['name'] = name_path
    news_link = item.xpath(".//a/@href")
    news['link'] = f'https://lenta.ru{news_link[0]}'
    news['date'] = item.xpath(".//time/@title")
    news['time'] = item.xpath(".//time[@class = 'g-time']/text()")
    collections.insert_one(news)

pprint(collections.find({}))





