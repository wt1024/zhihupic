# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class QuestionItem(scrapy.Item):
    questionid = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    answer_num = scrapy.Field() #回答个数
    attention_uv = scrapy.Field() #关注人数
    read_pv = scrapy.Field()      #阅读pv
    pass

class AnswerItem(scrapy.Item):
    answer_id = scrapy.Field()
    question_id = scrapy.Field()
    question_title = scrapy.Field()
    author_url_token = scrapy.Field()  #用户 唯一标示
    author_name = scrapy.Field()       #用户 昵称
    voteup_count = scrapy.Field()      #赞同数
    comment_count = scrapy.Field()     #评论数
    content = scrapy.Field()           #回答内容
    pass
# 因为mysqlpipilines里面根据 item的类型执行不同的sql
# 问题里爬的答案 和 收藏夹里爬的答案,我准备入到不同的表里
class AnswerItemForCollection(scrapy.Item):
    collection_name = scrapy.Field()
    collection_id = scrapy.Field()
    answer_id = scrapy.Field()
    question_id = scrapy.Field()
    question_title = scrapy.Field()
    author_url_token = scrapy.Field()  #用户 唯一标示
    author_name = scrapy.Field()       #用户 昵称
    voteup_count = scrapy.Field()      #赞同数
    comment_count = scrapy.Field()     #评论数
    content = scrapy.Field()           #回答内容
    pass

class MyImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
    question_answer_id = scrapy.Field()
