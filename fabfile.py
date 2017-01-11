from fabLib import *
from fabric.api import settings
import credentials

passwd = credentials.get_credentials()


def check_credentials(host):
    global passwd
    while True:
        if host in passwd:
            break
        credentials.add_credentials()
    passwd = credentials.get_credentials()


def test_run():
    host = raw_input('Host: ').strip()
    check_credentials(host)
    with settings(host_string=host, password=passwd[host], warn_only=True):
        # print mysql.add_user('linuxuser')
        # print mysql.add_tables(['linuxuser'])
        print mysql.del_user('linuxuser')

if __name__ == '__main__':
    test_run()