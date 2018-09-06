# -*- coding: utf-8 -*-

import hmac
import json
import scrapy
import time
import base64
from hashlib import sha1


class ZhihuLoginSpider(scrapy.Spider):
    name = 'zhihu_login'
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
    # 验证登录成功之后, 可以开始真正的爬取业务
    def check_login(self, response):
         # 验证是否登录成功
         text_json = json.loads(response.text)
         print(text_json)
         yield scrapy.Request('https://www.zhihu.com/inbox', headers=self.headers)

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

