from fabric.api import *
import templates
import re
import json
import base64

with open('CONFIG.json') as f:
    CONFIG = json.loads(f.read())

base64.b64decode(CONFIG['root'])


def get_users(pattern=None, verbose=True):
    db_string = run("mysql -uroot -p{0} -e 'SHOW DATABASES;'".format(base64.b64decode(CONFIG['root'])))
    db_list = map(lambda x: re.sub('_db$', '', x),
                 filter(lambda x: re.search('_db$', x),
                        __mysqlStringToList(db_string)))
    return templates.get_users_template(db_list)(pattern, verbose)


def add_users(add_list):
    return templates.add_users_template(get_users, __add_user)(add_list)


def del_users(pattern=None, del_list=[]):
    return templates.del_users_template(get_users, __del_user)(pattern, del_list)


def add_tables(user_list):
    fails = list()
    for username in user_list:
        code = run("mysql -uroot -p{0} {1}_db < /data/create_tbl.sql".format(base64.b64decode(CONFIG['root']),
                                                                             username))
        if code != 0:
            fails.append(username)
    return fails


def __add_user(username, password=None, group=None):
    return run('''
    mysql -uroot -p{0} -e 'CREATE DATABASE {1}_db;
    GRANT ALL ON {1}_db.* to \'{1}\'@\'localhost\';
    GRANT SELECT ON sqlexercise.* to \'{1}\'@\'localhost\';'
    '''.format(base64.b64decode(CONFIG['root']),
               username)).return_code


def __del_user(username):
    return run('''
    mysql -uroot -p{0} -e 'DROP USER \'{1}\'@\'localhost\''
    '''.format(base64.b64decode(CONFIG['root']),
               username))


def __mysqlStringToList(dbString):
    dbList = map(lambda x: x[1:-1].strip(), dbString.split('\r\n')[3:-1])
    return dbList