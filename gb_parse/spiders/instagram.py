import scrapy
import json
import datetime as dt
from ..items import InstaTag, InstaPost, InstaUser, InstaFollow


class InstagramSpider(scrapy.Spider):
    db_type = 'MONGO'
    name = "instagram"
    allowed_domains = ["www.instagram.com"]
    start_urls = ["https://www.instagram.com/"]
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    api_url = "/graphql/query/"
    query_hash = {
        "posts": "56a7068fea504063273cc2120ffd54f3",
        "tag_posts": "9b498c08113f1e09617a1703c22b2f32",
    }

    def __init__(self, login, password, *args, **kwargs):
        self.tags = ["geekbrains", "forzahorizon", "junior_developer"]
        self.login = login
        self.enc_passwd = password
        super().__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self.login_url,
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.enc_passwd,
                },
                headers={'X-CSRFToken': js_data['config']['csrf_token']}
            )
        except AttributeError:
            if response.json().get('authenticated'):
                for tag in self.tags:
                    yield response.follow(f'/explore/tags/{tag}', callback=self.tag_parse)

    def tag_parse(self, response):
        tag_data = self.js_data_extract(response)['entry_data']['TagPage'][0]['graphql']['hashtag']
        yield InstaTag(
            date_parse=dt.datetime.utcnow(),
            data={
                'id': tag_data['id'],
                'name': tag_data['name'],
                'profile_pic_url': tag_data['profile_pic_url'],
            }
        )
        yield from self.get_tag_posts(tag_data, response)

    def get_tag_posts(self, tag_data, response):
        if tag_data['edge_hashtag_to_media']['page_info']['has_next_page']:
            api_query = {
                'tag_name': tag_data['name'],
                'first': 2,
                'after': tag_data['edge_hashtag_to_media']['page_info']['end_cursor'],
            }
            url = f'/graphql/query/?query_hash={self.query_hash["tag_post"]}&variables={json.dumps(api_query)}'
            yield response.follow(
                url,
                callback=self.tag_api_parse,
            )
        yield from self.get_post_item(tag_data['edge_hashtag_to_media']['edges'])

    def get_post_item(self, edges, **kwargs):
        for node in edges:
            yield InstaPost(
                date_parse=dt.datetime.utcnow(),
                data=node['node'],
                image_urls=[node['node']['thumbnail_src']]
            )

    def tag_api_parse(self, response, **kwargs):
        yield from self.get_tag_posts(response.json()['data']['hashtag'], response)

    def js_data_extract(self, response):
        script = response.xpath('//script[contains(text(), "window._sharedData = ")]/text()').get()
        return json.loads(script.replace("window._sharedData = ", '')[:-1])