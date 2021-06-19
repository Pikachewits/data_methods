import scrapy
import re
from scrapy.http import HtmlResponse

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'вот тут вставляю логин'
    inst_pass = 'тут вставляю пароль из раздела enc_password'

    def parse(self, response):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callack=self.login,
            formdata={'username': self.inst_login, 'enc_password': self.inst_pass},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        print()

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')