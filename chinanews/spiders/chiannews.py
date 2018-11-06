# -*- coding: utf-8 -*-
# Created by dongzhi on 2018/11/5
import codecs
import time

import scrapy
from ..items import ChinanewsItem

class ChinaNewsSpider(scrapy.Spider):
    name = 'chinanews'
    start_urls = [
        'http://www.chinanews.com/scroll-news/ty/2018/1103/news.shtml'
    ]
    # base_url = 'http://www.chinanews.com'

    def parse(self, response):
        for li in response.xpath('//*[@id="content_right"]/div[@class="content_list"]/ul/li'):
            a = li.xpath("./div[2]/a")
            if len(a.extract()) > 0 :
                url = a.xpath("./@href").extract()[0]
                # title = a.xpath("./text()").extract()[0]
                # url = self.base_url + url
                # print(url,title)
                item = ChinanewsItem()
                item['url'] = url
                # 解析数据  开始时，此处的 meta_1 写成了 meat_1,浪费了不少测试时间
                yield scrapy.Request(url=url,meta={'meta_1':item}, callback=self.parse_content)

        # 添加url到 start_urls 列表中
        # add_urls = [
        #     'http://www.chinanews.com/scroll-news/ty/2018/1102/news.shtml'
        #     # 'http://www.chinanews.com/scroll-news/ty/2018/1101/news.shtml'
        # ]
        # for add_url in add_urls:
        #     yield response.follow(add_url,self.parse)

    def parse_content(self,response):
        item = response.meta['meta_1']
        # //*[@id="cont_1_1_2"]/div[6]/p[1]
        # //*[@id='cont_1_1_2']/div[8]/p/text()
        # //*[@id="cont_1_1_2"]/div[6]
        # //*[@id="backtop"]/div[6]/p
        # content 的解析开始时这样写 //*[@id='cont_1_1_2']/div[8]/p/text()
        # 每个网页结构不同，div[8] 不能通用，导致，有些网页的content内容为空，而不是 scrapy的丢数据（误认为）
        item['content'] = ''.join(response.xpath("//*[@id='cont_1_1_2']/div[@class='left_zw']/p/text()").extract())
        if item['content'] == '':
            item['content'] = ''.join(response.xpath("//*[@id='backtop']/div[@class='content_context']/p/text()").extract())
        # print(item['content'])
        if item['content'] != '':
            yield item
        # else:
        #     yield response.follow(item['url'], self.parse)

