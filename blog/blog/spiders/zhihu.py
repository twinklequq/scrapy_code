# -*- coding: utf-8 -*-
import scrapy
import urllib
import urllib3
import json
from urllib import parse
from ..items import ZhihuUserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blog.pipelines.DoubanPipeline': 100
        }
    }
    user_url = "https://www.zhihu.com/api/v4/members/{user}?"
    follower_url = "https://www.zhihu.com/api/v4/members/{user}/followers?"
    start_user = "tombkeeper"
    user_include = "allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics"
    follower_include = "data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics"
    offset = 0
    follower_params = {
        "include": follower_include,
        "offset": offset,
        "limit": 20
    }
    follower_params_encode = parse.urlencode(follower_params)
    user_param = {
        "include": user_include
    }
    user_param_encode = parse.urlencode(user_param)

    def start_requests(self):
        yield scrapy.Request(url=self.follower_url.format(user=self.start_user) + self.follower_params_encode, callback=self.parse_followee)

    def parse_followee(self, response):
        results = json.loads(response.text)
        paging = results['paging']
        user_infos = results['data']
        for user_info in user_infos:
            url_token = user_info['url_token']
            yield scrapy.Request(url=self.user_url.format(user=url_token) + self.user_param_encode, callback=self.parse_user)
        is_end = paging['is_end']
        if is_end == False:
            self.offset += 20
            self.follower_params['offset'] = self.offset
            self.follower_params_encode = parse.urlencode(self.follower_params)
        yield scrapy.Request(url=self.follower_url.format(user=self.start_user) + self.follower_params_encode, callback=self.parse_followee)

    def parse_user(self, response):
        item = ZhihuUserItem()
        user_info = json.loads(response.text)
        item['name'] = user_info['name']
        item['headline'] = user_info['headline']
        item['url'] = user_info['url']
        item['url_token'] = user_info['url_token']
        item['follower_count'] = user_info['follower_count']
        yield item



