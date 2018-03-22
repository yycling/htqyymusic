# -*- coding: utf-8 -*-
import scrapy
from song.spiders.py_bloomfilter import PyBloomFilter


class MusicSpider(scrapy.Spider):
    name = 'music'
    urls = list()
    for i in range(0, 15):
        url = "http://www.htqyy.com/genre/musicList/1?pageIndex={}&pageSize=20".format(i)
        urls.append(url)
    start_urls = urls
    bf = PyBloomFilter()

    def parse(self, response):
        """解析音频地址"""
        lis = list()
        t_list = response.xpath('//li[@class="mItem"]')
        for i in t_list:
            title = i.xpath("./span[@class='title']/a/@title").extract_first()
            sid = i.xpath("./span[@class='title']/a/@sid").extract_first()
            # 音频地址: http://f1.htqyy.com/play7/1569/mp3/3
            url = 'http://f1.htqyy.com/play7/' + sid + '/mp3/3'
            lis.append(url)
            # item["file_urls"] = lis
            artname = i.xpath("./span[@class='artistName']/a/text()").extract_first()
            name = title+'-'+artname
            bloom = self.bf.is_exist(url)
            if bloom == 0:  # 用布隆进行歌曲去重
                yield scrapy.Request(url,callback=self.parse_song,meta={"name":name})
                self.bf.add(url)

    def parse_song(self,response):
        """下载歌曲,保存到本地"""
        name = response.meta["name"]
        url = response.url
        song = response.body
        file_path = './htqyy/' + name + '.mp3'
        with open(file_path, "wb") as fp:  # 将音频保存到本地
            fp.write(song)
        with open('好听轻音乐歌曲.txt', 'a') as f:  # 已经下载的歌曲,将其信息保存到txt当中
            item = name+"  "+url
            f.write(item)
            f.write('\n')
        print("%s保存成功"%name)
