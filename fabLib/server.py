from fabLib import templates
from fabric.api import run, sudo


def get_users(pattern=None, verbose=None):
    '''
    Get users in Ubuntu server, tested on 216.230.228.88 and 216.230.228.82.
    :param pattern: a string pattern or regex object, matching user will be returned
    :param verbose: print string representation
    :return: a list of usernames. If pattern is not None, only returns the matching usernames)
    '''
    user_string = run('cat /etc/passwd').split('\r\n')
    user_string_filtered = filter(lambda x: x.find(':/home/') > 0, user_string)
    user_list = map(lambda user: user.split(':', 1)[0].strip(), user_string_filtered)
    return templates.get_users_template(user_list)(pattern, verbose)


def add_users(add_list):
    '''
    Add users to Ubuntu server, tested on 216.230.228.88 and 216.230.228.82.
    :param add_list: a list of (username,password)
    :return: a username list that fails to add
    '''
    return templates.add_users_template(get_users, __add_user)(add_list)


def del_users(pattern=None, del_list=[]):
    '''
    Delete users in Ubuntu server, tested on 216.230.228.88 and 216.230.228.82.
    :param pattern: a string pattern or regex object, matching user will be deleted
    :param del_list: a list of usernames to delete
    :return: a username list that fails to delete
    '''
    return templates.del_users_template(get_users, __del_user)(pattern, del_list)


def __add_user(username, password, group=None):
    if group is None:
        group = username
    sudo('''
    useradd {0}
    echo "{0}:{1}" | chpasswd
    mkdir /home/{0}
    cp /etc/bash.bashrc /home/{0}/.bashrc
    chown -R {0}:{2} /home/{0}/
    chsh -s /bin/bash {0}
    '''.format(username, password, group))


def __del_user(username):
    sudo('userdel -r {0}'.format(username))
