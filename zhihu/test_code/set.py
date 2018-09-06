
#!/usr/bin/python
import sys
import getopt
import MySQLdb


def main(argv=None):

    lst=['1','2','2']
    urls_unique = list(set(lst))
    print lst
    print urls_unique

    start_urls = ["https://www.zhihu.com/collection/19682978?page=3"]
    pages = 2
    
    for i in range(pages):
         print (start_urls[0]+"/page="+str(i+1))

if __name__ == "__main__":
    sys.exit(main())



