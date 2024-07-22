class BrokerAppDetails:

    def __init__(self, broker):
        self.broker = broker
        self.appKey = None
        self.appSecret = None
        self.pwd = None
        self.twofa = None
        self.totpKey = None
        self.apiKey = None
        self.tgBotToken = None
        self.apiBaseUrl = None
        self.webLoginUrl = None

    def setClientID(self, clientID):
        self.clientID = clientID

    def setAppKey(self, appKey):
        self.appKey = appKey

    def setAppSecret(self, appSecret):
        self.appSecret = appSecret

    def setPwd(self, pwd):
        self.pwd = pwd

    def setTwoFa(self, twofa):
        self.twofa = twofa

    def setTotpKey(self, totpKey):
        self.totpKey = totpKey

    def setApiKey(self, apiKey):
        self.apiKey = apiKey

    def setTgBotToken(self, tgBotToken):
        self.tgBotToken = tgBotToken

    def setApiBaseUrl(self, apiBaseUrl):
        self.apiBaseUrl = apiBaseUrl

    def setWebLoginUrl(self, webLoginUrl):
        self.webLoginUrl = webLoginUrl
