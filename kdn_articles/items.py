# -*- coding: utf-8 -*-
import scrapy

# items.py
class KdnArticlesItem(scrapy.Item):
    date_published = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    author_info = scrapy.Field()
    tags = scrapy.Field()
    excerpt = scrapy.Field()
    post_text = scrapy.Field()
    url = scrapy.Field()