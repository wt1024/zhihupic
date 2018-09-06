# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from zhihu.items import QuestionItem,AnswerItem,AnswerItemForCollection
class MysqlPipeline(object):
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "your password", "crawl", charset='utf8' )
        self.cursor = self.db.cursor()
    def process_item(self, item, spider):
        #insert_sql = 'insert into tianmu_bigpipe_delay(pipe_name, event_time, delay_range, percent) values '
        #insert_sql += "('%s', '%s', '%s', '%s')," % (row[0], event_time, row[3], row[4])
        if isinstance(item,QuestionItem):
            print("QuestionItem Mysql  insert begin ")
            insertsql="insert into zhihu_question (questionid,title,intro,answer_num,attention_uv,read_pv) values (%s,%s,%s,%s,%s,%s)" 
            param=(item['questionid'],item['title'],item['desc'],item['answer_num'],item['attention_uv'],item['read_pv'])
            try:
                self.cursor.execute(insertsql,param)
                self.db.commit()
            except Exception as e:
                print(e)
            print("QuestionItem Mysql  insert end  ")
        elif isinstance(item,AnswerItem):
            print ("AnswerItem Mysql insert begin ")
            insertsql="insert into zhihu_answer (answer_id,question_id,question_title,author_url_token,author_name,voteup_count,comment_count,content) values (%s,%s,%s,%s,%s,%s,%s,%s)" 
            param=(item['answer_id'],item['question_id'],item['question_title'],item['author_url_token'],item['author_name'],item['voteup_count'],item['comment_count'],item['content'])
            try:
                self.cursor.execute(insertsql,param)
                self.db.commit()
            except Exception as e:
                print(e) 
            print ("AnswerItem Mysql insert end ")
        elif isinstance(item,AnswerItemForCollection):
            print ("AnswerItemForCollection Mysql insert begin ")
            insertsql="insert into zhihu_answer_for_collection (collection_id,collection_name,answer_id,question_id,question_title,author_url_token,author_name,voteup_count,comment_count,content) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
            param=(item['collection_id'],item['collection_name'],item['answer_id'],item['question_id'],item['question_title'],item['author_url_token'],item['author_name'],item['voteup_count'],item['comment_count'],item['content'])
            try:
                self.cursor.execute(insertsql,param)
                self.db.commit()
            except Exception as e:
                print(e) 
            print ("AnswerItem MysqlForCollection insert end ") 
        else:
            print("no  item type error !!")
 
        #item['desc']=item['desc']+"testout"  #这里做处理,会影响输出文件到目录, 说明内置的文件输出在 pipelines中 级别很低
        return item
    
    def close_spider(self,spider):
        self.db.close()
