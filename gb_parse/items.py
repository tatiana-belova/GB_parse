import scrapy


class GbParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class InstaFollowed(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    follow_type = scrapy.Field()
    follow_name = scrapy.Field()
    follow_id = scrapy.Field()

class InstaFollowing(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    follow_type = scrapy.Field()
    follow_name = scrapy.Field()
    follow_id = scrapy.Field()