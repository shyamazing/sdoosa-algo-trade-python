import logging
import requests
import json
import pyotp

from config.Config import getSystemConfig
from loginmgmt.BaseLogin import BaseLogin
from .CryptoJsAES import CryptoJsAES
from pya3 import *


class AliceblueLogin(BaseLogin):
    def __init__(self, brokerAppDetails):
        BaseLogin.__init__(self, brokerAppDetails)

    def login(self, args):
        logging.info("==> AliceblueLogin .args => %s", args)
        systemConfig = getSystemConfig()

        # get encryption key
        url = self.brokerAppDetails.apiBaseURL + "/customer/getEncryptionKey"
        payload = json.dumps({"userId": self.brokerAppDetails.clientID})
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=True
        )
        encKey = response.json()["encKey"]
        checksum = CryptoJsAES.encrypt(
            self.brokerAppDetails.pwd.encode(), encKey.encode()
        ).decode("UTF-8")

        # login
        url = self.brokerAppDetails.apiBaseURL + "/customer/webLogin"
        payload = json.dumps(
            {"userId": self.brokerAppDetails.clientID, "userData": checksum}
        )
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=True
        )
        response_data = response.json()

        # pass two fa key
        url = self.brokerAppDetails.apiBaseURL + "/sso/2fa"
        payload = json.dumps(
            {
                "answer1": self.brokerAppDetails.twofa,
                "userId": self.brokerAppDetails.clientID,
                "sCount": str(response_data["sCount"]),
                "sIndex": response_data["sIndex"],
            }
        )
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=True
        )

        # verify totp
        totp = pyotp.TOTP(self.brokerAppDetails.totpKey)
        if (
            response.json()["loPreference"] == "TOTP"
            and response.json()["totpAvailable"]
        ):
            url = self.brokerAppDetails.apiBaseURL + "/sso/verifyTotp"
            payload = json.dumps(
                {"tOtp": totp.now(), "userId": self.brokerAppDetails.clientID}
            )
            headers = {
                "Authorization": "Bearer "
                + self.brokerAppDetails.clientID
                + " "
                + response.json()["us"],
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload, verify=True
            )

        # get response
        if response.json()["userSessionID"]:
            logging.info(
                "Aliceblue Login successful. userSessionID: ",
                response.json()["userSessionID"],
            )
        else:
            logging.info(
                "User is not TOTP enabled! Please enable TOTP through mobile or web",
                response.json(),
            )

        brokerHandle = Aliceblue(
            user_id=self.brokerAppDetails.clientID, api_key=self.brokerAppDetails.apiKey
        )
        session_id = brokerHandle.get_session_id()  # Get Session ID

        if session_id:
            # set broker handle and access token to the instance
            self.setBrokerHandle(brokerHandle)
            # redirect to home page with query param loggedIn=true
            homeUrl = systemConfig["homeUrl"] + "?loggedIn=true"
            logging.info("Aliceblue Redirecting to home page %s", homeUrl)
            redirectUrl = homeUrl
        else:
            loginUrl = brokerHandle.login_url()
            logging.info("Redirecting to zerodha login url = %s", loginUrl)
            redirectUrl = loginUrl
