import json
import base64
import os
import getpass

file_path = 'credentials.json'


def get_credentials(decode=True):
    if not os.path.exists(file_path):
        return dict()
    with open(file_path, 'r') as f:
        credentials = json.loads(f.read())
        if decode:
            for host in credentials:
                credentials[host] = base64.b64decode(credentials[host])
    return credentials


def add_credentials(host=None):
    if os.path.exists(file_path):
        credentials = get_credentials(decode=False)
    else:
        credentials = dict()
    while True:
        if not host:
            host = raw_input('add host (press enter to finish): ')
        if not host:
            break
        passwd = getpass.getpass('password for {0}: '.format(host))
        credentials[host] = base64.b64encode(passwd)
    with open(file_path, 'w') as f:
        json.dump(credentials, f)

if __name__ == '__main__':
    add_credentials()
    print get_credentials()
