import requests
import sys
from pprint import pprint
import logging
from khuauth.auth_handler import *

logging.basicConfig(level = logging.INFO)
def authenticate(user_id, user_pw):
    logging.info("Start khu authentication")
    session = requests.Session()
    account = {
        "user_id":user_id,
        "verified": False
    }
    try:
        info_21_login_request(session, user_id, user_pw)
        encrypted_login_form_obj = info_21_redirect_login_request(session)
        student_data = portal_login_request(
            session, encrypted_login_form_obj)
        account.update(student_data)
        account["verified"] = True
    except KhuAuthenticationException as e:
        logging.info(f'{user_id} has failed to authenticate by KHU')
    logging.info("Finish khu authentication")
    return account

if __name__ == "__main__":
    print(authenticate(sys.argv[1], sys.argv[2]))