from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader

from items import VacancyItem, EmployerItem


class VacancyLoader(ItemLoader):
    default_item_class = VacancyItem
    vac_name_out = TakeFirst()
    salary_out = ''.join
    vac_info_in = ''.join
    vac_info_out = TakeFirst()
    employer_url_out = TakeFirst()


class EmployerLoader(ItemLoader):
    default_item_class = EmployerItem
    emp_name_out = TakeFirst()
    url_out = TakeFirst()
    area_of_activity_out = TakeFirst()
    emp_description_in = ''.join
    emp_description_out = TakeFirst()
