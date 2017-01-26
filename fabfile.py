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
    pass


if __name__ == '__main__':
    test_run()
