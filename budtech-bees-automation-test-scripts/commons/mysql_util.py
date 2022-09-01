import mysql.connector

# 创建数据库连接


# 数据库连接
from commons.yaml_util import read_config_yaml, read_environment_yaml


#数据库类
def mysql_connect(service,database_name):
    my_con = mysql.connector.connect(
        host=read_environment_yaml(service)["HOST"],
        user=read_environment_yaml(service)["USER"],
        passwd=read_environment_yaml(service)["PASSWD"],
        port=read_environment_yaml(service)["PORT"],
        database=database_name,

    )
    return my_con


# 数据库查询所有
def mysql_select(service,database_name, sql):
    # 创建游标对象
    my_con = mysql_connect(service,database_name)
    my_cursor = my_con.cursor(dictionary=True)
    # 执行sql语句

    my_cursor.execute(sql)
    # 返回结果


    return my_cursor.fetchall()

# 数据库查询1条
def mysql_select_one(service,database_name, sql):
    # 创建游标对象
    my_con = mysql_connect(service,database_name)
    my_cursor = my_con.cursor(dictionary=True)
    # 执行sql语句

    my_cursor.execute(sql)
    # 返回结果

    return my_cursor.fetchone()

# 数据查询指定字段
def mysql_select_field(service,database_name, sql,field):
    """
    数据查询指定字段
    @param service: 服务
    @param database_name: 数据库名称
    @param sql:  sql语句
    @param field: 查询字段名
    @return: 返回字段值
    """
    all_data = mysql_select_one(service,database_name, sql)
    return all_data[field]


def mysql_connect_service(services,environment, sql,count=None):
    """
    连接entity，product数据库
    @param services: entity or product
    @param environment: dev or feature-5 or feature-test
    @param sql: sql语句
    @param count:  第几条
    @return: all_data
    """
    service = "MYSQL_CONNECT"
    database_name = ""
    if services == "entity":
        if str(environment).lower() == "dev" or str(environment).lower() == "feature-5":
            database_name = "bees_business_entity_dev"
        elif str(environment).lower() == "feature-test":
            database_name = "bees_bizentity_featuretest"
    elif services == "product":
        if str(environment).lower() == "dev" or str(environment).lower() == "feature-5":
            database_name = "bees_products_dev"
        elif str(environment).lower() == "feature-test":
            database_name = "bees_products_featuretest"
    all_data = mysql_select(service,database_name, sql)
    if count == None :
        return all_data[0]
    elif count == 0:
        return all_data
    else:
        return all_data[count-1]


# 数据库修改
def mysql_update(service,database_name, sql):
    # 创建游标对象
    my_con = mysql_connect(service,database_name)
    my_cursor = my_con.cursor()
    # 执行sql语句
    my_cursor.execute(sql)
    # 提交
    my_con.commit()
    # 返回结果
    return my_cursor.fetchone()


# 数据库删除
def mysql_rollback(service,database_name, sql):
    # 创建游标对象
    my_con = mysql_connect(service,database_name)
    my_cursor = my_con.cursor()
    # 执行sql语句
    my_cursor.execute(sql)
    # 提交
    my_con.commit()
    # 返回结果
    return my_cursor.fetchone()

