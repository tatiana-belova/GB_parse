import re
import scrapy

import pymongo


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']
    css_query = {
        'brands': '.TransportMainFilters_brandsList__2tIkv '
                  '.ColumnItemList_container__5gTrc .ColumnItemList_column__5gjdt a.blackLink'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = pymongo.MongoClient()['autoyoula_parse'][self.name]

    def parse(self, response):
        for link in response.css(self.css_query['brands']):
            yield response.follow(link.attrib['href'], callback=self.brand_page_parse)

    def brand_page_parse(self, response):
        for page in response.css('.Paginator_block__2XAPy a.Paginator_button__u1e7D'):
            yield response.follow(page.attrib['href'], callback=self.brand_page_parse)

        for item_link in response.css('article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu'):
            local_params = {'params': {'phone_number':
                            response.css('article.SerpSnippet_snippet__3O1t2 div.SerpSnippet_phone__2YAMr::text').get()}
                            }
            yield response.follow(item_link.attrib['href'], callback=self.ads_parse, cb_kwargs=local_params)

    def ads_parse(self, response, params):
        title = response.css('.AdvertCard_advertTitle__1S1Ak::text').get()
        images = response.css('section.PhotoGallery_thumbnails__3-1Ob button::attr(style)').re('(https?://[^\s]+)\)')
        characteristics = self.get_characteristics(response)
        description = response.css('.AdvertCard_descriptionInner__KnuRi::text').get()
        autor = self.js_decoder_autor(response)
        phone_number = params.get('phone_number')

        self.db.insert_one({
            'title': title,
            'images': images,
            'characteristics': characteristics,
            'description': description,
            'autor': autor,
            'phone_number': phone_number,
        })

    def js_decoder_autor(self, response):
        script = response.xpath('//script[contains(text(), "window.transitState =")]/text()').get()
        re_str = re.compile(r"youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar")
        result = re.findall(re_str, script)
        return f'https://youla.ru/user/{result[0]}' if result else None


    def get_characteristics(self, response):
        return {itm.css('.AdvertCharacteristics_elemTitle__2sK-L::text').get(): itm.css(
            '.AdvertCharacteristics_elemValue__3Vims::text').get() for itm in
                response.css('.AdvertCharacteristics_elemGroup__3ek5T')}