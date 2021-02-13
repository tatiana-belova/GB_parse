import os
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from GB_parse.gb_parse.spiders.instagram_1 import InstagramSpider

if __name__ == "__main__":
    load_dotenv(".env")
    crawler_settings = Settings()
    crawler_settings.setmodule("gb_parse.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(InstagramSpider, login=os.getenv("LOGIN"), password=os.getenv("PASSWORD"))
    crawler_process.start()