# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VacancyItem(scrapy.Item):
    _id = scrapy.Field()
    vac_name = scrapy.Field()
    salary = scrapy.Field()
    vac_info = scrapy.Field()
    key_skills = scrapy.Field()
    employer_url = scrapy.Field()

class EmployerItem(scrapy.Item):
        _id = scrapy.Field()
        emp_name = scrapy.Field()
        url = scrapy.Field()
        area_of_activity = scrapy.Field()
        emp_description = scrapy.Field()
        emp_vacancy_offer = scrapy.Field()
