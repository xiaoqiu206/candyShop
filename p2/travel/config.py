# coding=utf-8
'''
URL_LIST里存放网页地址,如果某个地址的数据不需要,在行首加 # 符号注释掉
'''
URL_LIST = (
        'http://zh.papillon.com/las-vegas-tours/bus-tours/grand-canyon-west-rim-bus-tour',
        'http://zh.papillon.com/las-vegas-tours/bus-tours/grand-canyon-west-rim-bus-tour-with-skywalk',
        'http://zh.papillon.com/las-vegas-tours/bus-tours/west-rim-bus-tour-with-helicopter-and-skywalk',
        'http://zh.papillon.com/las-vegas-tours/bus-tours/west-rim-bus-tour-with-helicopter',
        'http://zh.papillon.com/las-vegas-tours/bus-tours/west-rim-bus-tour-with-helicopter-boat-cruise-and-skywalk',
        'http://zh.papillon.com/las-vegas-tours/helicopter-with-skywalk-tours/skywalk-getaway-with-heli-and-boat',
        'http://zh.papillon.com/las-vegas-tours/bus-tours/grand-canyon-south-rim-bus-tour',
        'http://zh.papillon.com/las-vegas-tours/bus-tours/south-rim-bus-tour-with-helicopter',
        # 'http://www.baidu.com',
        )

SLEEP_TIME = 5  # 选择日期,点击确定后,等待响应的时间,单位是秒,如果网速慢,可以把这个时间设置长一点

DEADLINE_DAY = 30  # 获取从今天开始,往后几天的数据

UPLOAD_REMARK = False  # 本地数据库的remark是否同步到postgreSQL,True表示是,False表示否,,注意大小写

PGSQL_HOST = 'localhost'  # pgsql服务器ip
PGSQL_DBNAME = 'test'  # pgsql库名
PGSQL_USERNAME = 'postgres'  # pgsql用户名
PGSQL_PASSWORD = '123321'  # pgsql密码
PGSQL_PORT = '5432'  # pgsql端口


# 要上传的数据,请写在前后三引号之间,可以换行, "select * "请不要更改
SELECT_SQL = """
    select * from travel where 1=1
 
"""

