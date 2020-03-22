# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    #时间
    newsTime = scrapy.Field()

    #来源
    newsSource = scrapy.Field()

    #标题
    newsTitle = scrapy.Field()

    #链接
    newsLink = scrapy.Field()

    #关键字
    newsKeyword = scrapy.Field()




