import re
from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from .items import HhruItem

def get_companyname(header_string):
    return re.search(r'Вакансии компании (.*?) - работа в', header_string).group(1)


class HhruLoader(ItemLoader):
    default_item_class = HhruItem
    title_out = TakeFirst()
    url_out = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    salary_in = ''.join
    salary_out = TakeFirst()
    company_name_in = MapCompose(get_companyname)
    company_name_out = TakeFirst()
    company_website_out = TakeFirst()
    company_description_out = TakeFirst()
    company_tags = TakeFirst()