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
    # syan@216.230.228.82
    host = raw_input('Host: ').strip()
    check_credentials(host)
    with settings(host_string=host, password=passwd[host]):
        print hive.drop_tables('atn_cb')

if __name__ == '__main__':
    test_run()