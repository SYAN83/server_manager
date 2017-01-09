from fabric.api import *
import templates


def get_users(pattern=None, verbose=True):
    dbString = run("hive -e 'SHOW DATABASES'")
    dbList = __hiveStringToList(dbString)
    return templates.get_users_template(dbList)(pattern, verbose)


def add_users(add_list):
    return templates.add_users_template(get_users, __add_user)(add_list)


def del_users(pattern=None, del_list=[]):
    return templates.del_users_template(get_users, __del_user)(pattern, del_list)


def get_tables(database="default", pattern=None, verbose=True):
    tbl_string = run("hive -e 'SHOW TABLES IN {0};'".format(database))
    tbl_list = __hiveStringToList(tbl_string)
    return templates.get_users_template(tbl_list)(pattern, verbose)


def drop_tables(username):
    run('''
    hive -e 'SHOW TABLES IN {0}' | xargs -I '{{}}'\
    hive -e 'USE {0};DROP TABLE IF EXISTS {{}};DROP VIEW IF EXISTS {{}}'
    '''.format(username))


def __add_user(username, password=None, group=None):
    if group is None:
        group = username
    run("""hive -e 'CREATE DATABASE {0};\
    GRANT ALL ON DATABASE {0} TO USER {0};'
    hadoop fs -chown {0}:{1} /user/hive/warehouse/{0}.db
    """.format(username, group))


def __del_user(username):
    drop_tables(username)
    run("hive -e 'DROP DATABASE {0}'".format(username))


def __hiveStringToList(dbString):
    dbList = dbString.split("\r\nOK\r\n",1)[1].split("\r\nTime taken:")[0].split()
    return dbList