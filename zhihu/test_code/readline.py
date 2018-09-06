
#!/usr/bin/python
import sys
import getopt
import MySQLdb


def main(argv=None):

    file = open("/root/py_project/zhihu/zhihu/conf/start_questions.txt") 
    while 1:
        line = file.readline()
        line = line.strip('\n')
        if not line:
            break
        if(line[0:1] == "#"):
            print line
            pass
        print(line+"wangting")
    pass # do something
    file.close()




if __name__ == "__main__":
    sys.exit(main())



