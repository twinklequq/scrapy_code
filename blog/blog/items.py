# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    number = scrapy.Field()
    name = scrapy.Field()
    introduce = scrapy.Field()
    star = scrapy.Field()
    evaluate = scrapy.Field()
    image_urls = scrapy.Field()


class LagouItem(scrapy.Item):
    position_name = scrapy.Field()
    position_link = scrapy.Field()
    salary = scrapy.Field()
    experience = scrapy.Field()
    city = scrapy.Field()
    education = scrapy.Field()
    type = scrapy.Field()
    company = scrapy.Field()
    company_link = scrapy.Field()


class NeteaseItem(scrapy.Item):
    song_id = scrapy.Field()
    song = scrapy.Field()
    singer = scrapy.Field()
    album = scrapy.Field()
    lyric = scrapy.Field()


class ZhihuUserItem(scrapy.Item):
    pass


class AlexaItem(scrapy.Item):
    url = scrapy.Field()



