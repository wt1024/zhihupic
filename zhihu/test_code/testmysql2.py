
#!/usr/bin/python
import sys
import getopt
import MySQLdb


def main(argv=None):

    item={}
    item['answer_id']='11'
    item['question_id']='test title'
    item['question_title']='test describe'
    item['author_url_token']='10'
    item['author_name']='12'
    item['voteup_count']='13'
    item['comment_count']='13'
    item['content']='13sfsdfds<br?<p/>'

    db = MySQLdb.connect("localhost", "root", "111111", "crawl", charset='utf8' )
    cursor = db.cursor()
    insertsql="insert into zhihu_answer (answer_id,question_id,question_title,author_url_token,author_name,voteup_count,comment_count,content) values (%s,%s,%s,%s,%s,%s,%s,%s)"
    param=(item['answer_id'],item['question_id'],item['question_title'],item['author_url_token'],item['author_name'],item['voteup_count'],item['comment_count'],item['content'])
    try:
        self.cursor.execute(insertsql,param)
        self.db.commit()
    except Exception as e:
        print(e)
    print ("AnswerItem Mysql insert end ")
    #insertsql="insert into zhihu_question (questionid,title,intro,answer_num,attention_uv,read_pv) values  (%s,%s,%s,%s,%s,%s) "
    #insertsql+= "('%s', '%s', '%s', '%s', '%s', '%s')" % (item['questionid'],item['title'],item['desc'],item['answer_num'],item['attention_uv'],item['read_pv'])
    #param=(item['questionid'],item['title'],item['desc'],item['answer_num'],item['attention_uv'],item['read_pv'])
    print(insertsql)
    cursor.execute(insertsql,param)
    db.commit()
    db.close()





if __name__ == "__main__":
    sys.exit(main())



