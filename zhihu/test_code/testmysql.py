
#!/usr/bin/python
import sys
import getopt
import MySQLdb


def main(argv=None):


    str = "full/v2-93786db72221bc26cb4566c2a94009d5_r.jpg"
    print (str)
    print (str[5:][:-4])
    return
    item={}
    item['questionid']='a'
    item['title']='test title'
    item['desc']='test describe'
    item['answer_num']='10'
    item['attention_uv']='12'
    item['read_pv']='13'

    db = MySQLdb.connect("localhost", "root", "111111", "crawl", charset='utf8' )
    cursor = db.cursor()

    insertsql="insert into zhihu_question (questionid,title,intro,answer_num,attention_uv,read_pv) values "
    insertsql+= "('%s', '%s', '%s', '%s', '%s', '%s')" % (item['questionid'],item['title'],item['desc'],item['answer_num'],item['attention_uv'],item['read_pv'])
    param=(item['questionid'],item['title'],item['desc'],item['answer_num'],item['attention_uv'],item['read_pv'])
    print(insertsql)
    cursor.execute(insertsql)
    db.commit()
    db.close()





if __name__ == "__main__":
    sys.exit(main())



