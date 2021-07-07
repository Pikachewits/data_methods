import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from scrapy.loader import ItemLoader

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    insta_login = '***'
    insta_pwd = '***'
    parse_user = ['sonialime', 'tanyapomelnikova']  # Пользователи, у которых собираем посты.

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash = 'ea4baf885b60cbf664b34ee760397549'  # hash для получения данных по постах с главной страницы

    def parse(self, response: HtmlResponse):  # Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)  # csrf token забираем из html
        yield scrapy.FormRequest(  # заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:  # Проверяем ответ после авторизации
            yield response.follow(
                # Переходим на желаемую страницу пользователя.
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.parse_user}
            )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)  # Получаем id пользователя
        variables = {'count': 12,  # Формируем словарь для передачи даных в запрос
                     'search_surface': 'follow_list_page'}

        url_followers = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?{urlencode(variables)}'
        yield response.follow(url_followers,
                              headers={'User-Agent': 'Instagram 64.0.0.14.96'},
                              callback=self.user_posts_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'type': 'followers',
                                         'variables': deepcopy(variables)})

        url_following = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?{urlencode(variables)}'
        yield response.follow(url_following,
                              headers={'User-Agent': 'Instagram 64.0.0.14.96'},
                              callback=self.user_posts_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'type': 'following',
                                         'variables': deepcopy(variables)})

    def user_posts_parse(self, response: HtmlResponse, username, user_id, type,
                         variables):  # Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        users = j_data.get('users')
        for user in users:
            loader = ItemLoader(item=InstaparserItem(), response=response)
            loader.add_value('parent_name', username)
            loader.add_value('parent_id', user_id)
            loader.add_value('user_id', user.get('pk'))
            loader.add_value('name', user.get('full_name'))
            loader.add_value('photo', user.get('profile_pic_url'))
            loader.add_value('type', type)
            yield loader.load_item()

        next_page = j_data.get('next_max_id')
        if next_page:
            variables['max_id'] = next_page
            url = f'https://i.instagram.com/api/v1/friendships/{user_id}/{type}/?{urlencode(variables)}'

            yield response.follow(url,
                                  headers={'User-Agent': 'Instagram 64.0.0.14.96'},
                                  callback=self.user_posts_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'type': type,
                                             'variables': deepcopy(variables)}
                                  )

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')