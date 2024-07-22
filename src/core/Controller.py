import logging

from config.Config import getBrokerAppConfig
from models.BrokerAppDetails import BrokerAppDetails
from loginmgmt.ZerodhaLogin import ZerodhaLogin
from loginmgmt.AliceblueLogin import AliceblueLogin

class Controller:
  brokerLogin = None # static variable
  brokerName = None # static variable

  def handleBrokerLogin(args):
    brokerAppConfig = getBrokerAppConfig()

    brokerAppDetails = BrokerAppDetails(brokerAppConfig['broker'])
    brokerAppDetails.setClientID(brokerAppConfig['clientID'])
    
    brokerAppDetails.setPwd(brokerAppConfig['pwd'])
    brokerAppDetails.setTwoFa(brokerAppConfig['twofa'])
    brokerAppDetails.setTotpKey(brokerAppConfig['tOtpKey'])
    brokerAppDetails.setApiKey(brokerAppConfig['apiKey'])
    brokerAppDetails.setTgBotToken(brokerAppConfig['tgBotToken'])
    brokerAppDetails.setApiBaseUrl(brokerAppConfig['apiBaseUrl'])
    brokerAppDetails.setWebLoginUrl(brokerAppConfig['webLoginUrl'])

    logging.info('handleBrokerLogin appKey %s', brokerAppDetails.appKey)
    Controller.brokerName = brokerAppDetails.broker
    if Controller.brokerName == 'zerodha':
      Controller.brokerLogin = ZerodhaLogin(brokerAppDetails)
    elif Controller.brokerName == 'aliceblue':
      Controller.brokerLogin = AliceblueLogin(brokerAppDetails)

    redirectUrl = Controller.brokerLogin.login(args)
    return redirectUrl

  def getBrokerLogin():
    return Controller.brokerLogin

  def getBrokerName():
    return Controller.brokerName
