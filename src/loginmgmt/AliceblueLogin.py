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
            loginUrl = self.brokerAppDetails.webLoginUrl
            logging.info("Redirecting to alice blue login url = %s", loginUrl)
            redirectUrl = loginUrl

        return redirectUrl
