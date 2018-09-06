# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import getopt
import MySQLdb
import json
import random
import string
from lxml import etree

def random_string(size=13, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def main(argv=None):
    
    rana = random_string()
    ranb = random_string()
    print(rana)
    print(ranb)

    #return 
    f = open('/var/www/html/scrapy/answer/52') 
    contents = f.read()
    print(contents)
    f.close()
    
    #print(contents)
    res=json.loads(contents)
    #print (res)
    data=res['data']
    # 一次返回多个(默认5个)答案, 需要遍历
    for od in data:
        #print(od)
        print(od['id'])  #  answer id
        print(od['question']['id'])  #问题id
        print(od['question']['title'])  #question title
        print(od['author']['url_token']) #user token
        print(od['author']['name'])      #user name 
        print('赞同: '+ str(od['voteup_count']))
        print("评论: "+str(od["comment_count"]))
        print(od['content'])   #内容 
        testh = etree.HTML(od['content'])
        allurls=','.join(testh.xpath("//img/@data-original"))
        print(allurls)
        for i in testh.xpath("//img/@data-original"):
            print (i)
        print("#####3")


if __name__ == "__main__":
    sys.exit(main())



