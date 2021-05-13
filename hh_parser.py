from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re

search_vacancy = 'Python'


def parser_hh(search_vacancy):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    domain = 'https://hh.ru'
    url = '/search/vacancy/'
    vacancies = []
    params = {'text': search_vacancy, 'search_field': 'name', 'page': 0}

    for page in range(0, 40):
        params['page'] = page
        response = requests.get(domain + url, params=params, headers=headers)
        dom = bs(response.text, 'html.parser')
        vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item'})
        try:
            dom.find('a', {'data-qa': 'pager-next'}).find('span')
            for vacancy in vacancy_list:
                vacancies.append(hh_data(vacancy))
        except:
            break

    return vacancies


def hh_data(search_vacancy):
    vacancy_dict = {}

    vacancy_name = search_vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()
    vacancy_dict['vacancy_name'] = vacancy_name

    salary = search_vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary_currency = None
    if not salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText().replace(u'\u202f', u'')
        salary = re.split(r'\s|-', salary)
        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
            salary_currency = str(salary[2])
        elif salary[0] == 'от':
            salary_min = int(salary[1])
            salary_max = None
        else:
            salary_min = int(salary[0])
            salary_max = int(salary[2])
            salary_currency = str(salary[3])
    vacancy_dict['salary_min'] = salary_min
    vacancy_dict['salary_max'] = salary_max
    vacancy_dict['salary_currency'] = salary_currency

    vacancy_link = search_vacancy.find('a',{'class':'bloko-link'})['href']
    vacancy_dict['vacancy_link'] = vacancy_link

    return vacancy_dict


pprint(parser_hh(search_vacancy))