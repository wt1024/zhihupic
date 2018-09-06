
#!/usr/bin/python
import sys
import getopt
import MySQLdb


def main(argv=None):

    db = MySQLdb.connect("localhost", "root", "your password", "crawl", charset='utf8' )
    cursor = db.cursor()

    selectsql="select questionid,answer_num from  zhihu_question limit 2;"
    print(selectsql)
    answer_template="https://www.zhihu.com/api/v4/questions/%s/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics&limit=5&offset=%s&sort_by=default"
    try:
        cursor.execute(selectsql)    
        results = cursor.fetchall()
        for row in results:
            questionid = row[0]
            answer_num = row[1]
            #tem = questionid+"  "+answer_num
            print "%s  %s " % (questionid, answer_num)
            fornum = answer_num/5
            for i in range(fornum+1):
                temurl = answer_template % (str(questionid), str(i*5))
                print temurl
                print i*5

    except Exception as e:
        print(e)
    db.close()





if __name__ == "__main__":
    sys.exit(main())



