# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import NeteaseItem
from ..utils import encrypt


class NeteaseSpider(scrapy.Spider):
    name = 'netease'
    allowed_domains = ['music.163.com']
    base_url = "https://music.163.com"
    # start_urls = ['https://music.163.com/']
    start_urls = ['https://music.163.com/discover/playlist/?cat=%E5%8F%A4%E9%A3%8E']

    def parse(self, response):

        node_list = response.xpath("//div[@class='g-wrap p-pl f-pr']/ul[@class='m-cvrlst f-cb']/li")
        for node in node_list:
            playlist_url = self.base_url + node.xpath(".//div[@class='u-cover u-cover-1']/a//@href").extract_first()
            yield scrapy.Request(url=playlist_url, callback=self.parse_playlist)
        next_page = response.xpath("//div[@class='u-page']//a[@class='zbtn znxt']/@href").extract_first()
        if next_page:
            next_url = self.base_url + next_page
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_playlist(self, response):
        song_list = response.css("ul.f-hide li a::attr(href)").extract()
        for song in song_list:
            full_song = self.base_url + song
            id = song.split('=')[1]
            request = scrapy.Request(url=full_song, callback=self.parse_song)
            request.meta['id'] = id
            yield request

    def parse_song(self, response):
        id = response.meta['id']
        song = response.css("div.tit em::text").extract_first()
        singer = response.css("a.s-fc7[href*='/artist?id=']::text").extract_first()
        album = response.css("a.s-fc7[href*='/album?id=']::text").extract_first()
        params, encSecKey = encrypt.get_params(id)
        payload = {
            'params': params,
            'encSecKey': encSecKey
        }
        meta_dict = {
            'song_id': id,
            'song': song,
            'singer': singer,
            'album': album
        }
        url = "https://music.163.com/weapi/song/lyric?csrf_token="
        yield scrapy.FormRequest(url=url, formdata=payload, callback=self.parse_lyric, meta=meta_dict)

    def parse_lyric(self, response):
        item = NeteaseItem()
        result = json.loads(response.text)
        lyric = result['lrc']['lyric']
        re_lyric = re.sub(r'[\d:.[\]]', '', lyric)
        item['song_id'] = response.meta['song_id']
        item['song'] = response.meta['song']
        item['singer'] = response.meta['singer']
        item['album'] = response.meta['album']
        item['lyric'] = re_lyric
        yield item




