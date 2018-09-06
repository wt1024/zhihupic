# -*- coding: utf-8 -*-
import random
import string
import hmac
import json
import scrapy
import time
import base64
from hashlib import sha1
import MySQLdb
from lxml import etree
from zhihu.items import AnswerItem
from zhihu.items import MyImageItem
class AnswerSpider(scrapy.Spider):
    name = 'answer'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
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
         #'scrapy.pipelines.images.ImagesPipeline': 6  #这个是scrapy自带的图片下载pipelines
        }   
    }
    answer_template="https://www.zhihu.com/api/v4/questions/%s/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics&limit=5&offset=%s&sort_by=default"
    # 验证登录成功之后, 可以开始真正的爬取业务
    def check_login(self, response):
         # 验证是否登录成功
         text_json = json.loads(response.text)
         print(text_json)
         #yield scrapy.Request('https://www.zhihu.com/inbox', headers=self.headers)
         #从mysql中读取question的信息,来进行爬取
         db = MySQLdb.connect("localhost", "root", "111111", "crawl", charset='utf8' )
         cursor = db.cursor()
         # 301,23,303,304,114
         selectsql="select questionid,answer_num from  zhihu_question where id in ( 251,138,93,233,96,293,47,24,288,151,120,311,214,33) ;"
         # 251,138,93,233,96,293,47,24,288,151,120,311,214,33
         print(selectsql)
       
         try:
             cursor.execute(selectsql)    
             results = cursor.fetchall()
             for row in results:
                 questionid = row[0]
                 answer_num = row[1]
                 fornum = answer_num/5
                 print("questionid : "+ str(questionid)+"   answer_Num: "+str(answer_num))
                 for i in range(fornum+1):
                     answer_url = self.answer_template % (str(questionid), str(i*5))
                     print("current answer url :  " + answer_url)
                     yield scrapy.Request(answer_url,callback=self.parse_answer, headers=self.headers) 
         except Exception as e:
             print(e)
         db.close()


    def parse_answer(self,response):
        #测试时把返回结果写到本次
        #temfn= str(random.randint(0,100))
        #f = open("/var/www/html/scrapy/answer/"+temfn,'wb')
        #f.write(response.body)
        #f.write("------")
        #f.close() 
        res=json.loads(response.text)
        #print (res)
        data=res['data']
        # 一次返回多个(默认5个)答案, 需要遍历
        for od in data:
            #print(od)
            item = AnswerItem()
            item['answer_id']=str(od['id'])  #  answer id
            item['question_id']=str(od['question']['id'])
            item['question_title']=od['question']['title']
            item['author_url_token']=od['author']['url_token']
            item['author_name']=od['author']['name']
            item['voteup_count']=str(od['voteup_count'])
            item['comment_count']=str(od["comment_count"])
            item['content']=od['content']
            yield item
            testh = etree.HTML(od['content'])
            itemimg = MyImageItem()
            
            itemimg['question_answer_id'] = str(od['question']['id'])+"/"+str(od['id'])
            itemimg['image_urls']=testh.xpath("//img/@data-original")
            yield itemimg
            #for imgurl in testh.xpath("//img/@data-original"):
            #    itemimg = MyImageItem()
            #    itemimg['images']=od['id']
            #    itemimg['image_urls']=imgurl 
            #    print(imgurl)
            #    yield itemimg


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

