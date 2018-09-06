# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import getopt
import MySQLdb
import json
import random
import string
from lxml import etree
import errno
def random_string(size=13, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def main(argv=None):
    

    #return 
    f = open('/var/www/html/scrapy/answer/15') 
    contents = f.read()
    #print(contents)
    f.close()
    testh = etree.HTML(contents)
    itemlist = testh.xpath('//div[@id="zh-list-collection-wrap"]/div[@data-type="Answer"]')
    print(testh.xpath('//*[@id="zh-fav-head-title"]/text()'))
    print(itemlist)
    for item in itemlist:
        #test2=etree.HTML(etree.tostring(item))
        test2=item
        print(test2.xpath('.//h2[@class="zm-item-title"]/a/text()')[0])    #question title
        print(test2.xpath('.//h2[@class="zm-item-title"]/a/@href')[0].split('/')[2])  #question id . /question/22781195
        print(test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/@data-atoken')[0])  #answer id
        try:
            print(test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/div[@class="answer-head"]/div[@class="zm-item-answer-author-info"]/span/span[@class="author-link-line"]/a/text()')[0])  # 昵称
            print(test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/div[@class="answer-head"]/div[@class="zm-item-answer-author-info"]/span/span[@class="author-link-line"]/a/@href')[0].split('/')[2])  #用户唯一token
        except IndexError as e:
            pass
        print(test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/div[@data-action="/answer/content"]/textarea/text()')[0]) #内容
        #question 也找到了接口返回 answer信息, 其中点赞,评论为数字
        # 这里 collection页, 爬的浏览器地址, 赞和评论有可能是  1,003  或者 15k,  数据库里存的改成了 字符串
        print(test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/div[@class="zm-item-vote"]/a/text()')[0])  #赞
        print(test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/div[@class="zm-item-meta answer-actions clearfix js-contentActions"]/div[@class="zm-meta-panel"]/a[@name="addcomment"]/text()')[1].split(" ")[0])  # 评论
        print("****")
        print("********")


if __name__ == "__main__":
    sys.exit(main())



