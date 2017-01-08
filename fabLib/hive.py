from fabric.api import *
import templates


def get_users(pattern=None, verbose=True):
    dbString = run("hive -e 'SHOW DATABASES'")
    dbList = __hiveStringToList(dbString)
    return templates.get_users_template(dbList)(pattern, verbose)


def create_users(add_list):
    return templates.create_users_template(get_users, __add_user)(add_list)


def remove_users(pattern=None, remove_list=[]):
    return templates.remove_users_template(get_users, __del_user)(pattern, remove_list)


def get_tables(database="default", pattern=None, verbose=True):
    tblString = run("hive -e 'SHOW TABLES IN {0};'".format(database))
    tblList = __hiveStringToList(tblString)
    return templates.get_users_template(tblList)(pattern, verbose)


def drop_tables(username):
    run('''
    hive -e 'SHOW TABLES IN {0}.db' | xargs -I '{{}}'
    hive -e 'USE {0}.db;DROP TABLE IF EXISTS {{}};DROP VIEW IF EXISTS {{}}'
    '''.format(username))


def __add_user(username, password=None, group=None):
    if group is None:
        group = username
    run("""hive -e 'CREATE DATABASE {0};\
    GRANT ALL ON DATABASE {0} TO USER {0};'
    hadoop fs -chown {0}:{1} /user/hive/warehouse/{0}.db
    """.format(username, group))


def __del_user(username):
    database = username + '.db'
    drop_tables(database)
    run("hive -e 'DROP DATABASE {0}'".format(database))


def __hiveStringToList(dbString):
    dbList = dbString.split("\r\nOK\r\n",1)[1].split("\r\nTime taken:")[0].split()
    return dbList