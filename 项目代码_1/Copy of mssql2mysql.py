#!/usr/bin python
#coding=utf-8

"""
用作比较大小的唯一识别字段是
YTH_CLJCXXB.yth_jylsh
"""

import MySQLdb
import pymssql
import time

#定时配置
sec = 60      #秒,填写一个整数,每隔sec秒执行同步

#mysql的配置
mysql_host = "localhost"   #IP
mysql_port = "3306"   #端口
mysql_database = "DX"  #库名
mode3_table = "mode3"      #表名
mode6_table = "mode6"       #表名
mysql_user = "root"      #用户名
mysql_password = "root"   #密码

#sqlsever的配置
mssql_host = "192.168.1.4"    #IP
mssql_port = "1433"     #端口
mssql_database = "yth_new"   #库名
mssql_user = "sa"       #用户名
mssql_password = "888666"   #密码

def getMssqlconn():
    conn = pymssql.connect(
                    host=mssql_host,
                    user=mssql_user,
                    password=mssql_password,
                    database=mssql_database,
                    charset="UTF-8"
                    )
    return conn

#获得mysql连接
def getMysqlconn():
    conn = MySQLdb.connect(
                    host=mysql_host,
                    user=mysql_user,
                    passwd=mysql_password,
                    db=mysql_database
                    )
    return conn

def getMode3MaxID():
    mysqlcon = getMysqlconn()
    mysqlCursor = mysqlcon.cursor()
    mysqlCursor.execute("select max(SHIBIE) from %s.%s"% (mysql_database,mode3_table))
    row = mysqlCursor.fetchone()
    if len(row) == 1:
        maxID = row[0]
    else:
        maxID = None
    return maxID

def getMode6MaxID():
    mysqlcon = getMysqlconn()
    mysqlCursor = mysqlcon.cursor()
    mysqlCursor.execute("select max(SHIBIE) from %s.%s"% (mysql_database,mode6_table))
    row = mysqlCursor.fetchone()
    if len(row) == 1:
        maxID = row[0]
    else:
        maxID = None
    return maxID
    
def getMssql3Data():
    mode3_sql = """
        SELECT     hjyw_jcjg.JCFFID, hjyw_jcjg.JCZT, hjyw_jcjg.HCPFXZ, hjyw_jcjg.HCPFJG, hjyw_jcjg.HCPFPD, hjyw_jcjg.COPFXZ, hjyw_jcjg.COPFJG, hjyw_jcjg.COPFPD, 
                      hjyw_jcjg.NOXPFXZ, hjyw_jcjg.NOXPFJG, hjyw_jcjg.NOXPFPD, hjyw_jcjg.HCNOXXZ, hjyw_jcjg.HCNOXJG, hjyw_jcjg.HCNOXPD, hjyw_jcjg.ZDLBGLXZ, 
                      hjyw_jcjg.SCZDLBGL, hjyw_jcjg.FDJEDZSSX, hjyw_jcjg.FDJEDZSXX, hjyw_jcjg.SCFDJEDZS, hjyw_jcjg.LDPFXZ, hjyw_jcjg.PFJG100, hjyw_jcjg.PFJG90, 
                      hjyw_jcjg.PFJG80, hjyw_gcsj.HCGCSJ, hjyw_gcsj.COGCSJ, hjyw_gcsj.CO2GCSJ, hjyw_gcsj.O2GCSJ, hjyw_gcsj.NOXGCSJ, hjyw_gcsj.GLKQXSSJ, 
                      hjyw_gcsj.HCPFZLGCSJ, hjyw_gcsj.COPFZLGCSJ, hjyw_gcsj.NOXPFZLGCSJ, hjyw_gcsj.LLJO2GCSJ, hjyw_gcsj.LLJSJLLGCSJ, hjyw_gcsj.LLJBZLLGCSJ, 
                      hjyw_gcsj.LLJWDGCSJ, hjyw_gcsj.QCWQLLGCSJ, hjyw_gcsj.LLJQYGCSJ, hjyw_gcsj.ZSGCSJ, hjyw_gcsj.YWGCSJ, hjyw_gcsj.CSGCSJ, hjyw_gcsj.XSBGCSJ, 
                      hjyw_gcsj.XSXZGCSJ, hjyw_gcsj.SDXZGCSJ, hjyw_gcsj.JSGLGCSJ, hjyw_gcsj.ZSGLGCSJ, hjyw_gcsj.HJWDGCSJ, hjyw_gcsj.HJSDGCSJ, hjyw_gcsj.HJDQYGCSJ, 
                      hjyw_gcsj.YDZGCSJ, hjyw_gcsj.GXSXSGCSJ, YTH_CLJCXXB.yth_jylsh
FROM         hjyw_gcsj FULL OUTER JOIN
                      hjyw_jcjg ON hjyw_gcsj.hjlsh = hjyw_jcjg.hjjylsh FULL OUTER JOIN
                      YTH_CLJCXXB INNER JOIN
                      YTH_HJLSXXB ON YTH_CLJCXXB.yth_jylsh = YTH_HJLSXXB.yth_jylsh ON hjyw_jcjg.hjjylsh = YTH_HJLSXXB.hjjylsh
WHERE     (hjyw_jcjg.JCFFID = 3) AND (hjyw_jcjg.JCZT = 1) AND (hjyw_jcjg.COPFJG > '5') AND (hjyw_jcjg.NOXPFJG > '1')
    
    """
    mssqlcon = getMssqlconn()
    mssqlCursor = mssqlcon.cursor()
    mode3_maxid = getMode3MaxID()
    print 'mode3_maxid:',mode3_maxid
    if mode3_maxid is None:
        mssqlCursor.execute(mode3_sql)
    else:
        mssqlCursor.execute(mode3_sql + ' and YTH_CLJCXXB.yth_jylsh > %s',(mode3_maxid,))
    dataList = mssqlCursor.fetchall()
    return dataList

def getMssql6Data():
    mode3_sql = """
        SELECT     hjyw_jcjg.JCFFID, hjyw_jcjg.JCZT, hjyw_jcjg.HCPFXZ, hjyw_jcjg.HCPFJG, hjyw_jcjg.HCPFPD, hjyw_jcjg.COPFXZ, hjyw_jcjg.COPFJG, hjyw_jcjg.COPFPD, 
                      hjyw_jcjg.NOXPFXZ, hjyw_jcjg.NOXPFJG, hjyw_jcjg.NOXPFPD, hjyw_jcjg.HCNOXXZ, hjyw_jcjg.HCNOXJG, hjyw_jcjg.HCNOXPD, hjyw_jcjg.ZDLBGLXZ, 
                      hjyw_jcjg.SCZDLBGL, hjyw_jcjg.FDJEDZSSX, hjyw_jcjg.FDJEDZSXX, hjyw_jcjg.SCFDJEDZS, hjyw_jcjg.LDPFXZ, hjyw_jcjg.PFJG100, hjyw_jcjg.PFJG90, 
                      hjyw_jcjg.PFJG80, hjyw_gcsj.HCGCSJ, hjyw_gcsj.COGCSJ, hjyw_gcsj.CO2GCSJ, hjyw_gcsj.O2GCSJ, hjyw_gcsj.NOXGCSJ, hjyw_gcsj.GLKQXSSJ, 
                      hjyw_gcsj.HCPFZLGCSJ, hjyw_gcsj.COPFZLGCSJ, hjyw_gcsj.NOXPFZLGCSJ, hjyw_gcsj.LLJO2GCSJ, hjyw_gcsj.LLJSJLLGCSJ, hjyw_gcsj.LLJBZLLGCSJ, 
                      hjyw_gcsj.LLJWDGCSJ, hjyw_gcsj.QCWQLLGCSJ, hjyw_gcsj.LLJQYGCSJ, hjyw_gcsj.ZSGCSJ, hjyw_gcsj.YWGCSJ, hjyw_gcsj.CSGCSJ, hjyw_gcsj.XSBGCSJ, 
                      hjyw_gcsj.XSXZGCSJ, hjyw_gcsj.SDXZGCSJ, hjyw_gcsj.JSGLGCSJ, hjyw_gcsj.ZSGLGCSJ, hjyw_gcsj.HJWDGCSJ, hjyw_gcsj.HJSDGCSJ, hjyw_gcsj.HJDQYGCSJ, 
                      hjyw_gcsj.YDZGCSJ, hjyw_gcsj.GXSXSGCSJ, YTH_CLJCXXB.yth_jylsh
FROM         hjyw_gcsj FULL OUTER JOIN
                      hjyw_jcjg ON hjyw_gcsj.hjlsh = hjyw_jcjg.hjjylsh FULL OUTER JOIN
                      YTH_CLJCXXB INNER JOIN
                      YTH_HJLSXXB ON YTH_CLJCXXB.yth_jylsh = YTH_HJLSXXB.yth_jylsh ON hjyw_jcjg.hjjylsh = YTH_HJLSXXB.hjjylsh
WHERE     (hjyw_jcjg.JCFFID = 6) AND (hjyw_jcjg.JCZT = 1) AND (hjyw_jcjg.PFJG100 > '0.8')
    
    """
    mssqlcon = getMssqlconn()
    mssqlCursor = mssqlcon.cursor()
    mode6_maxid = getMode6MaxID()
    print 'mode6_maxid:',mode6_maxid
    if mode6_maxid is None:
        mssqlCursor.execute(mode3_sql)
    else:
        mssqlCursor.execute(mode3_sql + ' and YTH_CLJCXXB.yth_jylsh > %s',(mode6_maxid,))
    dataList = mssqlCursor.fetchall()
    return dataList

def updateMysql6():
    dataList6 = getMssql6Data()  
    print "sqlsever的数据行数是:",len(dataList6)
    sql= "insert into " + mode6_table +""" ( 
           JCFFID,
           JCZT,
           HCPFXZ,
           HCPFJG, 
           HCPFPD,
           COPFXZ,
           COPFJG,
           COPFPD, 
           NOXPFXZ, 
           NOXPFJG,
           NOXPFPD,
           HCNOXXZ,
           HCNOXJG,
           HCNOXPD,
           ZDLBGLXZ, 
           SCZDLBGL,
           FDJEDZSSX,
           FDJEDZSXX,
           SCFDJEDZS,
           LDPFXZ,
           PFJG100, 
           PFJG90, 
           PFJG80,
           HCGCSJ,
           COGCSJ,
           CO2GCSJ,
           O2GCSJ, 
           NOXGCSJ,
           GLKQXSSJ, 
           HCPFZLGCSJ,
           COPFZLGCSJ,
           NOXPFZLGCSJ,
           LLJO2GCSJ,
           LLJSJLLGCSJ,
           LLJBZLLGCSJ, 
           LLJWDGCSJ,
           QCWQLLGCSJ,
           LLJQYGCSJ,
           ZSGCSJ,
           YWGCSJ,
           CSGCSJ,
           XSBGCSJ, 
           XSXZGCSJ,
           SDXZGCSJ,
           JSGLGCSJ,
           ZSGLGCSJ,
           HJWDGCSJ,
           HJSDGCSJ,
           HJDQYGCSJ, 
           YDZGCSJ,
           GXSXSGCSJ,
           SHIBIE
           )values(
       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,     
       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
       %s,%s
            );                       
"""
    mysqlCon = getMysqlconn()
    mysqlCursor = mysqlCon.cursor()
    mysqlCursor.execute("use %s;"% mysql_database)
    count = 0
    for each in dataList6:
        try:
            mysqlCursor.execute(sql,each)
        except:
            print "mode6操作失败"
            pass
        mysqlCon.commit()
        count+=1
    print u"mode6插入%d行" % count

def updateMysql3():
    dataList3 = getMssql3Data()  
    print "sqlsever的数据行数是:",len(dataList3)
    sql= "insert into " + mode3_table +"""( 
           JCFFID,
           JCZT,
           HCPFXZ,
           HCPFJG, 
           HCPFPD,
           COPFXZ,
           COPFJG,
           COPFPD, 
           NOXPFXZ, 
           NOXPFJG,
           NOXPFPD,
           HCNOXXZ,
           HCNOXJG,
           HCNOXPD,
           ZDLBGLXZ, 
           SCZDLBGL,
           FDJEDZSSX,
           FDJEDZSXX,
           SCFDJEDZS,
           LDPFXZ,
           PFJG100, 
           PFJG90, 
           PFJG80,
           HCGCSJ,
           COGCSJ,
           CO2GCSJ,
           O2GCSJ, 
           NOXGCSJ,
           GLKQXSSJ, 
           HCPFZLGCSJ,
           COPFZLGCSJ,
           NOXPFZLGCSJ,
           LLJO2GCSJ,
           LLJSJLLGCSJ,
           LLJBZLLGCSJ, 
           LLJWDGCSJ,
           QCWQLLGCSJ,
           LLJQYGCSJ,
           ZSGCSJ,
           YWGCSJ,
           CSGCSJ,
           XSBGCSJ, 
           XSXZGCSJ,
           SDXZGCSJ,
           JSGLGCSJ,
           ZSGLGCSJ,
           HJWDGCSJ,
           HJSDGCSJ,
           HJDQYGCSJ, 
           YDZGCSJ,
           GXSXSGCSJ,
           SHIBIE
           ) values(
       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,     
       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
       %s,%s
            );
                        
"""
    mysqlCon = getMysqlconn()
    mysqlCursor = mysqlCon.cursor()
    mysqlCursor.execute("use %s;"% mysql_database)
    count = 0
    for each in dataList3:
        try:
            mysqlCursor.execute(sql,each)
        except:
            print "mode3操作失败"
        mysqlCon.commit()
        count+=1
    print u"mode3插入%d行" % count

while True:       
    updateMysql3()
    updateMysql6()
    time.sleep(sec)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    