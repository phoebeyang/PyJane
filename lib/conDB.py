#encoding=utf-8

import MySQLdb
import json
from log import *

MYSQL_HOST = "xx.xx.xx.xx"
MYSQL_USER = "xxxx"
MYSQL_PASSWD = "xxxx"
MYSQL_PORT = 3306

def query_mysql(sql,db,host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,port=MYSQL_PORT):
    try:
        con = MySQLdb.connect(host=host,user=user,passwd=passwd,db=db,port=port,charset='utf8')  
        cur = con.cursor(cursorclass = MySQLdb.cursors.DictCursor)#dict type of output
        print sql
        count = cur.execute(sql)
        results = cur.fetchall()
        #results = cur.fetchmany(count)
        print results
        return results
        cur.close()
    except MySQLdb.Error,e:
        print "Mysql Erro %d : %s " % (e.args[0],e.args[1])
        setLog("Mysql Erro %d : %s " % (e.args[0],e.args[1]),level="error")
    




if __name__ == "__main__":
    sql = 'select contents from user_sites where uid=73873795 and type=1'
    res = query_mysql(sql,'browser')
    print res
    print json.loads(res[0][0])
