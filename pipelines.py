# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

REDIS_URL = 'localhost'


class SongPipeline(object):
    def process_item(self, item, spider):
        with open('好听轻音乐歌曲.txt', 'a') as f:
            json.dump(item, f, ensure_ascii=False)
            print('\n')
        return item
