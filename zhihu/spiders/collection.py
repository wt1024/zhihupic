# -*- coding: utf-8 -*-

import random
import hmac
import json
import scrapy
import time
import base64
from hashlib import sha1
from scrapy import Spider,Request
from zhihu.items import AnswerItemForCollection
from zhihu.items import MyImageItem
from lxml import etree

class CollectionSpider(scrapy.Spider):
    name = 'collection'
    allowed_domains = ['www.zhihu.com']
    #start_urls = ['http://www.zhihu.com/']
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    # agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',

        'Referer': 'https://www.zhihu.com/signup?next=%2F',
        'User-Agent': agent,
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
    }
    grant_type = 'password'
    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    timestamp = str(int(time.time() * 1000))
    timestamp2 = str(time.time() * 1000)
    print(timestamp)
    print(timestamp2)
    
    custom_settings = {
        'ITEM_PIPELINES' : {
         'zhihu.mysqlpipelines.MysqlPipeline': 5,
         'zhihu.myimagepipelines.MyImagesPipeline' : 6
         #'scrapy.pipelines.images.ImagesPipeline': 1, #这个是scrapy自带的图片下载pipelines
        }
    }
    ############################### 需要修改的地方
    #收藏夹一般指定url,所以用start_urls   并且手动填写总页数!!!
    start_urls = ["https://www.zhihu.com/collection/38624707"]
    #总页数  
    pages = 81 

    # 验证登录成功之后, 可以开始真正的爬取业务
    def check_login(self, response):
         # 验证是否登录成功
         text_json = json.loads(response.text)
         print(text_json)
         for i in range(self.pages):
             url=self.start_urls[0]+"?page="+str(i+1)
             print(url)
             yield scrapy.Request(url,callback=self.parse_collection, headers=self.headers)

         #yield scrapy.Request('https://www.zhihu.com/question/26037846',callback=self.parse_question, headers=self.headers)
         #yield scrapy.Request('https://www.zhihu.com/question/60660517',callback=self.parse_question, headers=self.headers)
         #yield scrapy.Request('https://www.zhihu.com/inbox',self.parse_question, headers=self.headers)
         #for url in self.start_urls:
         #   #self.headers[':path']=url
         #   yield Request(url,callback = self.parse_question,headers = self.headers)
         #   #time.sleep(5)a
         




    def parse_collection(self,response):
        print (response.url)
        #print (response.text)
        #temfn= str(random.randint(0,100))
        #f = open("/var/www/html/scrapy/answer/"+temfn,'wb')
        #f.write(response.body)
        #f.write("------")
        #f.close() 
        itemlist=response.selector.xpath('//div[@id="zh-list-collection-wrap"]/div[@data-type="Answer"]') 
        #print(itemlist)
        print("##")
        #print(response.text)
        print("###")
        #print(itemlist)
        #print(response.body)
        collectionid=self.start_urls[0].split("/")[4]
        collection_name=response.selector.xpath('//*[@id="zh-fav-head-title"]/text()').extract()[0]
        #print(collection_name)
        for item in itemlist:
            #test2=etree.HTML(etree.tostring(item))
            test2=item
            coll_item = AnswerItemForCollection()
            coll_item['collection_id']=collectionid
            coll_item['question_title']=test2.xpath('.//h2[@class="zm-item-title"]/a/text()').extract()[0]    #question title
            coll_item['question_id']=test2.xpath('.//h2[@class="zm-item-title"]/a/@href').extract()[0].split('/')[2]  #question id . /question/22781195
            coll_item['answer_id']=test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/@data-atoken').extract()[0]  #answer id
            try:
                coll_item['author_name']=test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/div[@class="answer-head"]/div[@class="zm-item-answer-author-info"]/span/span[@class="author-link-line"]/a/text()').extract()[0]  # 昵称
                coll_item['author_url_token']=test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/div[@class="answer-head"]/div[@class="zm-item-answer-author-info"]/span/span[@class="author-link-line"]/a/@href').extract()[0].split('/')[2]  #用户    唯一token
            except IndexError as e:
                pass
            coll_item['content']=test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/div[@data-action="/answer/content"]/textarea/text()').extract()[0] #内容
            #question 也找到了接口返回 answer信息, 其中点赞,评论为数字
            # 这里 collection页, 爬的浏览器地址, 赞和评论有可能是  1,003  或者 15k,  数据库里存的改成了 字符串
            coll_item['voteup_count']=test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/div[@class="zm-item-vote"]/a/text()').extract()[0]  #赞 
            coll_item['comment_count']=test2.xpath('.//div[@class="zm-item-fav"]/div[@class="zm-item-answer "]/div[@class="zm-item-meta answer-actions clearfix js-contentActions"]/div[@class="zm-meta-panel"]/a[@name="addcomment"]/text()').extract()[1].split(" ")[0]  # 评论  
            print("****")
            print("********")
            coll_item['collection_name']=collection_name
            yield coll_item
            testh = etree.HTML(coll_item['content'])
            itemimg = MyImageItem()
    
            itemimg['question_answer_id'] = str(coll_item['question_id'])+"/"+str(coll_item['answer_id'])
            itemimg['image_urls']=testh.xpath("//img/@data-original")
            yield itemimg
    def get_signature(self, grant_type, client_id, source, timestamp):
        """处理签名"""
        hm = hmac.new(b'd1b964811afb40118a12068ff74a12f4', None, sha1)
        hm.update(str.encode(grant_type))
        hm.update(str.encode(client_id))
        hm.update(str.encode(source))
        hm.update(str.encode(timestamp))
        return str(hm.hexdigest())

    def parse(self, response):
        print("****************")
        print(response.url)
        #print(response.body.decode("utf-8"))

    def start_requests(self):
        yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                             headers=self.headers, callback=self.is_need_capture)

    def is_need_capture(self, response):
        print(response.text)
        need_cap = json.loads(response.body)['show_captcha']
        print(need_cap)

        if need_cap:
            print('需要验证码')
            yield scrapy.Request(
                url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                headers=self.headers,
                callback=self.capture,
                method='PUT'
            )
        else:
            print('不需要验证码')
            post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
            post_data = {
                "client_id": self.client_id,
                "username": "",  # 输入知乎用户名
                "password": "",  # 输入知乎密码
                "grant_type": self.grant_type,
                "source": self.source,
                "timestamp": self.timestamp,
                "signature": self.get_signature(self.grant_type, self.client_id, self.source, self.timestamp),  # 获取签名
                "lang": "en",
                "ref_source": "homepage",
                "captcha": '',
                "utm_source": "baidu"
            }
            yield scrapy.FormRequest(
                url=post_url,
                formdata=post_data,
                headers=self.headers,
                callback=self.check_login
            )
        # yield scrapy.Request('https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000),
        #                      headers=self.headers, callback=self.capture, meta={"resp": response})
        # yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
        #                      headers=self.headers, callback=self.capture, meta={"resp": response},dont_filter=True)

    def capture(self, response):
        # print(response.body)
        try:
            img = json.loads(response.body)['img_base64']
        except ValueError:
            print('获取img_base64的值失败！')
        else:
            img = img.encode('utf8')
            img_data = base64.b64decode(img)

            with open('/var/www/html/scrapy/zh.gif', 'wb') as f:
                f.write(img_data)
                f.close()
        captcha = raw_input('请输入验证码：')
        post_data = {
            'input_text': captcha
        }
        yield scrapy.FormRequest(
            url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
            formdata=post_data,
            callback=self.captcha_login,
            headers=self.headers
        )

    def captcha_login(self, response):
        try:
            cap_result = json.loads(response.body)['success']
            print(cap_result)
        except ValueError:
            print('关于验证码的POST请求响应失败!')
        else:
            if cap_result:
                print('验证成功!')
        post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        post_data = {
            "client_id": self.client_id,
            "username": "",  # 输入知乎用户名
            "password": "",  # 输入知乎密码
            "grant_type": self.grant_type,
            "source": self.source,
            "timestamp": self.timestamp,
            "signature": self.get_signature(self.grant_type, self.client_id, self.source, self.timestamp),  # 获取签名
            "lang": "en",
            "ref_source": "homepage",
            "captcha": '',
            "utm_source": ""
        }
        headers = self.headers
        headers.update({
            'Origin': 'https://www.zhihu.com',
            'Pragma': 'no - cache',
            'Cache-Control': 'no - cache'
        })
        yield scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=headers,
            callback=self.check_login
        )

