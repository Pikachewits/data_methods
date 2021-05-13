from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re

search_vacancy = 'Python'


def parser_sj(search_vacancy):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    domain = 'https://www.superjob.ru'
    url = '/vacancy/search/'
    vacancies = []
    params = {'keywords': search_vacancy,'page': 0}

    for page in range(0, 40):
        params['page'] = page
        response = requests.get(domain + url, params=params, headers=headers)
        dom = bs(response.text, 'html.parser')
        vacancy_list = dom.find_all('div', {'class': 'f-test-vacancy-item'})
        for vacancy in vacancy_list:
            vacancies.append(sj_data(vacancy))

    return vacancies


def sj_data(search_vacancy):
    vacancy_dict = {}

    vacancy_name = search_vacancy.find('a', {'class': '_6AfZ9'}).text
    vacancy_dict['vacancy_name'] = vacancy_name

    vacancy_link = 'https://www.superjob.ru' + search_vacancy.find('a', {'class': '_2JivQ'})['href']
    vacancy_dict['vacancy_link'] = vacancy_link

    return vacancy_dict


pprint(parser_sj(search_vacancy))