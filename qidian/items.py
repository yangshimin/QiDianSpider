# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    novel_id = scrapy.Field()
    novel_title = scrapy.Field()
    novel_author = scrapy.Field()
    novel_type = scrapy.Field()
    novel_state = scrapy.Field()
    novel_intro = scrapy.Field()
    novel_updated_words = scrapy.Field()
    novel_cid = scrapy.Field()


# class QiDianDetailItem(scrapy.Item):
    # honor = scrapy.Field()
    lasted_update = scrapy.Field()
    update_time = scrapy.Field()
    month_vote_num = scrapy.Field()
    week_reward_num = scrapy.Field()

