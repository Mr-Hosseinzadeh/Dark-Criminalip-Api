import json
import random
import requests as req
from tempmail import EMail
from bs4 import BeautifulSoup
import time
from urllib.parse import unquote

class Temp_Mail:

    def __init__(self) -> None:
        self.headers = {
        "Cookie": "_locale=en;",
        "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "Dnt": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }
        self.get_user_agent()
        self.email = EMail()
        print(self.email)
        while "ezztt" in self.email.address or "icznn.com" in self.email.address or "1secmail.com" in self.email.address:
            self.email = EMail()
    
    def __enter__(self):
        return self
    
    def __exit__(self,exc_type, exc_value, traceback):
        self.headers = {}

    url = "https://www.criminalip.io/api"
    password = "@Test12345678!"


    def get_user_agent(self):
        path = "user-agent.txt"
        with open(path, "r+", encoding="utf-8") as file:
            user_aganets = file.readlines()
            random_number = random.randrange(0, user_aganets.__len__())
            user_aganet = user_aganets[random_number].removesuffix("\n")
            self.headers["User-Agent"] = user_aganet

    def signup(self):
        url_signup = self.url + "/auth/user/signup"
        data = {
            "account_type": "not_social",
            "email": f"{self.email}",
            "uid": "",
            "name": f"{self.email}",
            "pw": self.password,
            "pp_agree_code": 1,
            "tos_agree_code": 1,
            "ad_agree_code": 1,
        }
        response = req.post(url_signup, headers=self.headers, json=data)
        dict_result = json.loads(response.text)
        if dict_result["status"] == 200:
            time.sleep(2)
            return self.send_verfiy(response)
        

    def send_verfiy(self, last_response):
        url_authentication = self.url + "/email/authentication"
        self.headers["Cookie"] = (
            self.headers["Cookie"]
            + last_response.headers["set-cookie"].split(";")[0]
            + ";"
        )
        
        response = req.post(url_authentication, headers=self.headers)
        dict_result = json.loads(response.text)
        if not response.headers["set-cookie"]:
            pass
        self.headers["Cookie"] = (
            self.headers["Cookie"] + response.headers["set-cookie"].split(";")[0] + ";"
        )

        if dict_result["status"] == 200:
            time.sleep(2)
            return self.get_token_verify()
        

    def get_token_verify(self):
        try:
            msg = self.email.wait_for_message(timeout=60)
        except:
            self.__init__()
        html_doc = msg.html_body
        soup = BeautifulSoup(html_doc, "html.parser")
        a_tags = soup.find_all("a")
        url_verify = a_tags[0].get("href")
        response = req.get(url_verify, headers=self.headers)
       

        if response.status_code == 200:
            time.sleep(1)
            token = url_verify.split("token=")[1]
            token = unquote(token)
            return self.verfiy(token)
        

    def verfiy(self, token):
        url_authToken = self.url + "/auth/user/authToken"
        # self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = {
            "auth_token": f"{token}"
        }
        response = req.post(url_authToken, headers=self.headers, data=data,)
        dict_result = json.loads(response.text)
        # self.headers["Content-Type"] = "application/json"
        if dict_result["status"] == 200:
            time.sleep(2)
            return self.login()
        

    def login(self):
        url_login = self.url + "/auth/user/login"
        data = {
            "account_type": "not_social",
            "email": f"{self.email}",
            "pw": self.password,
        }
        # self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        response = req.post(url_login, headers=self.headers, data=data)
        dict_result = json.loads(response.text)
        # self.headers["Content-Type"] = "application/json"
        if dict_result["status"] == 200:
            time.sleep(1)
            return self.get_apikey()
        

    def get_apikey(self):
        url_get_apikey = "https://www.criminalip.io/api/proxy/account/mypage/get-info"
        response = req.get(url_get_apikey, headers=self.headers)
        dict_result = json.loads(response.text)
        if dict_result["status"] == 200:
            dict_result = json.loads(response.text)
            api_key = dict_result["data"]["api_key"][0]["key"]

            return api_key
        


def main():
    
    with Temp_Mail() as temp_mail:
        api_key = temp_mail.signup()
    if api_key:
        return api_key
    else:
        main()
 
