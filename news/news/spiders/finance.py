# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem


class FinanceSpider(scrapy.Spider):
    # 爬虫名，启动爬虫时需要的参数
    name = 'finance'
    # 爬取域范围，允许爬虫在这个域名下进行爬取(可选)
    allowed_domains = []
    # url列表，爬虫执行后第一批请求，将从这个列表获取
    page = 2
    # 并发爬取
    # start_urls =  ['http://news.21so.com/chanye/'+ str(page)+ '.html' for page in range(2, 6)]
    start_urls = ['http://news.21so.com/chanye/index.html', 'http://news.21so.com/chanye/' + str(page) + '.html', ]

    def parse(self, response):
        # print(response.body.decode())
        node_list = response.xpath('//div[@class="textBox"]')
        for node in node_list:
            item = NewsItem()
            # 提取每条新闻的信息
            # 标题
            item['newsTitle'] = node.xpath('./h5/a/text()').extract()[0]
            # 关键字
            if len(node.xpath('./div[@class="tags"]/a/text()')):
                item['newsKeyword'] = node.xpath('./div[@class="tags"]/a/text()').extract()
            else:
                item['newsKeyword'] = ""
            # 链接
            item['newsLink'] = node.xpath('./h5/a/@href').extract()[0]

            detail_url = node.xpath('./h5/a/@href').extract()[0]
            # print(type(detail_url), detail_url, "00000000000000000000000000000000000000000000000000")
            yield scrapy.Request(url=detail_url, callback=self.detail_parse, meta={"item": item})

            # yield item
        # 构建下一页请求
        if int(self.page) < 6:
            self.page += 1
            url = 'http://news.21so.com/chanye/' + str(self.page) + '.html'
            yield scrapy.Request(url, callback=self.parse)

    def detail_parse(self, response):
        item = response.meta["item"]
        node_list = response.xpath('//div[@class="articleInfo"]')
        for node in node_list:
            item['newsSource'] = node.xpath('normalize-space(./span[@class="articleSource"]/text())').extract()[0]
            item['newsTime'] = node.xpath('normalize-space(./span[@class="articleDate"]/text())').extract()[0]

            yield item
