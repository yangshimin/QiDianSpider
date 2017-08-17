# -*- coding: utf-8 -*-
import scrapy
import json

from ..items import QidianItem


class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['http://m.qidian.com/majax/category/list?_csrfToken=9G16iHOJWlYWT7GE8PEjIqOBHl1X0JL3oEWnXSOI&gender=male&pageNum=1&orderBy=&catId=21&subCatId=']
    base_detail_url = 'http://m.qidian.com/book/{id}'
    base_url = 'http://m.qidian.com/majax/category/list?_csrfToken=9G16iHOJWlYWT7GE8PEjIqOBHl1X0JL3oEWnXSOI&gender=male&pageNum={page}&orderBy=&catId=21&subCatId='

    def parse(self, response):
        res = json.loads(response.body_as_unicode())
        pageMax = res['data']['pageMax']
        novel_pro_list = res['data']['records']
        page_num = res['data']['pageNum'] + 1
        for novel in novel_pro_list:
            item = QidianItem()
            item['novel_author'] = novel['bAuth']
            item['novel_title'] = novel['bName']
            item['novel_id'] = novel['bid']
            item['novel_type'] = novel['cat']
            item['novel_cid'] = novel['cid']
            item['novel_updated_words'] = novel['cnt']
            item['novel_intro'] = novel['desc']
            item['novel_state'] = novel['state']

            yield scrapy.Request(self.base_detail_url.format(id=novel['bid']), meta={'item': item}, callback=self.parse_detail_item)

        if page_num <= pageMax:
            yield scrapy.Request(url=self.base_url.format(page=page_num), callback=self.parse)


    def parse_detail_item(self, response):
        item = response.meta['item']
        # 防止在请求中发生偶然的错误
        # if response.status in self.handle_httpstatus_list:
        #     item['lasted_update'] = ' '
        #     item['update_time'] = ' '
        #     item['month_vote_num'] = ' '
        #     item['week_reward_num'] = ' '
        #     yield item

        # honor = response.css('.detail strong::text').extract()[0]
        # lasted_update = response.css('.detail .cf .blue::text').extract()[0]
        item['lasted_update'] = response.xpath('//*[@id="ariaMuLu"]/text()[1]').extract()[0]
        # update_time = response.css('.detail .time::text').extract()[0]
        item['update_time'] = response.xpath('//*[@id="ariaMuLu"]/text()[2]').extract()[0]
        # month_vote_num = response.css('#monthCount::text').extract()[0]
        item['month_vote_num'] = response.css('.book-pay-p .month-ticket-cnt::text').extract()[0]
        # week_reward_num = response.css('#rewardNum::text').extract()[0]
        item['week_reward_num'] = response.css('.recomm-ticket-rank::text').extract()[0]

        yield item
