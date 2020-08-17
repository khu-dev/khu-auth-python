import requests
import sys
from pprint import pprint
import logging
from khuauth.handler.auth import khu


def authenticate(user_id, user_pw, univ_name = 'khu'):
    account = {}
    if univ_name == 'khu':
        account = khu.authenticate(user_id, user_pw)
    return account


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) == 3:
        print(authenticate(sys.argv[1], sys.argv[2]))
    elif len(sys.argv) == 4:
        print(authenticate(sys.argv[1], sys.argv[2], sys.argv[3]))
    else:
        print("Wrong input")