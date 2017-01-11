from fabric.api import *
import re


def get_users_template(user_list):

    def get_users(pattern=None, verbose=True):
        users = user_list
        if pattern is not None:
            users = filter(lambda user: re.search(pattern, user), users)
        if verbose:
            print '\n'.join(users)
        return users

    return get_users


def add_users_template(get_users_func, add_user_func):

    def add_users(add_list):
        fails = []
        existing = get_users_func(verbose=False)
        for user in add_list:
            if isinstance(user, str):
                username, password = user, None
            else:
                username, password = user
            if username in existing:
                print 'User {0} exists.\n'.format(username)
                fails.append(username)
                continue
            else:
                code = add_user_func(username, password)
                if code != 0:
                    fails.append(username)
        if fails:
            print 'Unable to add the following users:'
            print '\n'.join(fails)
        return fails

    return add_users


def del_users_template(get_users_func, del_user_func):
    def del_users(pattern, del_list):
        if pattern is None and not del_list:
            print 'No user to delete.'
            return []
        users = get_users_func(verbose=False)
        fails = []
        if del_list:
            users = list(set(users).intersection(del_list))
        for username in users:
            if pattern is None or re.search(pattern, username):
                to_remove = prompt('Are you sure you want to delete {0}? Y/n:'.format(username))
                if to_remove == 'Y':
                    code = del_user_func(username)
                    if code != 0:
                        fails.append(username)
        if fails:
            print 'Unable to delete the following users:'
            print '\n'.join(fails)
        return fails

    return del_users

if __name__ == '__main__':
    pass