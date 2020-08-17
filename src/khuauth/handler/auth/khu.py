import sys
import requests, json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pprint import pprint
import logging
from khuauth import config


class KhuAuthenticationException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


def info_21_login_request(session, user_id, user_pw):
    logging.debug("Start info_21_login_request")
    r = session.post(config.INFO_21_LOGIN_URL,
        data={"userId": user_id,
            "userPw": user_pw,
            "loginRequest": ""
        },
        headers={"Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": config.USER_AGENT, "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"},
        )
    logging.debug(r.text)
    logging.debug("Finish info_21_login_request")
    return r.text


def info_21_redirect_login_request(session):
    logging.debug("Start info_21_redirect_login_request")
    r = session.get(config.INFO_21_REDIRECT_URL, headers={"User-Agent": config.USER_AGENT})
    soup = BeautifulSoup(r.text, "html.parser")
    logging.debug(soup)
    encrypted_form = soup.find(id="ssoLoginForm")
    if encrypted_form == None:
        # FAIL LOGIN
        raise KhuAuthenticationException("Failed info_21_redirect_login_request")
    encrypted_obj = {}
    for input_elem in encrypted_form.find_all("input"):
        encrypted_obj[input_elem["name"]] = input_elem["value"]
    logging.debug("Print info_21_redirect_login_request")
    return encrypted_obj


def portal_login_request(session, input_data):
    logging.debug("Start portal_login_request")
    r = session.post(config.PORTAL_LOGIN_URL, input_data, headers={
        "Content-Type": "application/x-www-form-urlencoded", "User-Agent": config.USER_AGENT})
    if r.status_code != 200:
        raise KhuAuthenticationException("Failed portal_login_request")

    logging.debug(r.text)
    json_string = r.text.split(
        "var global=")[1].split("</script>")[0].split(";var globalMain")[0]
    parsed_json = json.loads(json_string)
    student_data = {
        "student_number": parsed_json['userId']
    }
    logging.debug("Finish portal_login_request")

    return student_data



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
    logging.basicConfig(level=logging.INFO)
    print(authenticate(sys.argv[1], sys.argv[2]))