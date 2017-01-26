from fabLib import templates
from fabric.api import run, hosts


def get_users(pattern=None, verbose=True):
    '''
    Get users in hadoop cluster, tested on namenode 216.230.228.82.
    :param pattern: a string pattern or regex object, matching user will be returned
    :param verbose: print string representation
    :return: a list of usernames. If pattern is not None, only returns the matching usernames)
    '''
    userString = run('hadoop fs -ls /user/').split('\n')
    userList = map(lambda x: x[1].strip(),
                   filter(lambda x: len(x) > 1,
                          map(lambda x: x.split(' /user/'), userString)))
    return templates.get_users_template(userList)(pattern, verbose)


def add_users(add_list):
    '''
    Add users to hadoop cluster, tested on namenode 216.230.228.82.
    :param add_list: a list of (username,password)
    :return: a username list that fails to add
    '''
    return templates.add_users_template(get_users, __add_user)(add_list)


def del_users(pattern=None, del_list=[]):
    '''
    Delete users in hadoop cluster, tested on namenode 216.230.228.82.
    :param pattern: a string pattern or regex object, matching user will be deleted
    :param del_list: a list of usernames to delete
    :return: a username list that fails to delete
    '''
    return templates.del_users_template(get_users, __del_user)(pattern, del_list)


def log_permission():
    log_path = '/usr/local/hadoop-2.7.1/logs/hadoop.log'
    run('sudo chown hadoop:hadoop {0};sudo chmod a+w {0}'.format(log_path))


def hadoop_busniss_add_file(user_list):
    fails = list()
    for username in user_list:
        code = run('''
        hadoop fs -put /data3/aetna-track-1/* /user/{0}/;
        hadoop fs -chown {0}:{0} /user/{0}/Diagnosis_Code.csv;
        hadoop fs -chown {0}:{0} /user/{0}/hospital_discharge.csv;
        '''.format(username))
        if code != 0:
            fails.append(username)
    return fails


def __add_user(username, password=None, group=None):
    if group is None:
        group = username
    run('''
    hadoop fs -mkdir /user/{0}
    hadoop fs -chown -R {0}:{1} /user/{0}
    '''.format(username, group))


def __del_user(username):
    run('hadoop fs -rm -r /user/{0}'.format(username))