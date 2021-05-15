from pymongo import MongoClient
from pprint import pprint
from Lesson_2.hh_parser import parser_hh

hh_vacancies = parser_hh(search_vacancy='Проектировщик')

client = MongoClient('127.0.0.1', 27017)

db = client['headhunter_vac']
collections = db.hh_collection


for vacancy in hh_vacancies:
    collections.update_one({'vacancy_link': vacancy['vacancy_link']}, {"$set": vacancy}, upsert=True)

my_salary = 300000

count = 0
for collection in collections.find({"$or": [{'salary_min': {"$gt": my_salary}}, {'salary_max': {"$gt": my_salary}}]}):
    count +=1
    pprint(collection)
    print(count)

