# -*- coding: utf-8 -*-


import codecs
import json
import pymysql
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class BlogPipeline(object):
    def process_item(self, item, spider):
        return item


class DoubanPipeline(object):
    def __init__(self):
        print("start writing")
        self.file = codecs.open(filename='zhihu.json', mode='w+', encoding='utf-8')

    def process_item(self, item, spider):
        res = dict(item)
        str = json.dumps(res, ensure_ascii=False)
        self.file.write(str)
        self.file.write(',\n')
        return item

    def close_spider(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open("zhihuexporter.json", "w+")
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class NeteaseMongodbPipeline(object):
    def __init__(self, host, port, db, collection):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection
        self.client = None
        self.conn = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MONGODB_HOST'),
            port=crawler.settings.get('MONGODB_PORT'),
            db=crawler.settings.get('MONGODB_DB'),
            collection=crawler.settings.get('MONGODB_COLLECTION'),
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.host, self.port)
        self.conn = self.client[self.db]

    def process_item(self, item, spider):
        content = dict(item)
        self.conn[self.collection].insert(content)
        return item

    # def close_spider(self, spider):
    #     self.client.close()