from pymongo import MongoClient
from lxml import html
import requests
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['lenta_news']
collections = db.yandex_collection


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

response = requests.get('https://yandex.ru/news/')
dom = html.fromstring(response.text)


items = dom.xpath("//div[@class ='mg-grid__row mg-grid__row_gap_8 news-top-rubric-flexible-stories news-app__top'][1]//div[@class = 'mg-grid__col mg-grid__col_xs_4' or @class = 'mg-grid__col mg-grid__col_xs_6']")

for item in items:
    news ={}
    news['link'] = item.xpath(".//div[@class = 'mg-card__text']/a/@href")
    name_path = item.xpath(".//h2[@class='mg-card__title']/text()")[0].replace('\xa0', ' ')
    news['news'] = name_path
    news['resource'] = item.xpath(".//a/text()")
    news['time'] = item.xpath(".//span[@class = 'mg-card-source__time']/text()")
    collections.insert_one(news)

pprint(collections.find({}))