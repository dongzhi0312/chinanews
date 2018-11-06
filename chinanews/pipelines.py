# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ChinanewsPipeline(object):
    def process_item(self, item, spider):
        # base_dir = os.getcwd()
        # print(item['content'])
        filename ='./data/sport/' + item['url'].split('//')[-1].replace('/','_').split('.')[-2].replace('com_','') + '.txt'
        # print(filename)
        with open(filename, 'w',encoding='utf-8') as f:
            f.write(item['content'])
        return item
