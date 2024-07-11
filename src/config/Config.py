import json
import os


def getpath(setting_name):
    # Determine the directory of the current script
    setting_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "settings",
        setting_name,
    )
    return setting_dir


def getServerConfig():
    with open(getpath("server.json"), "r") as server:
        jsonServerData = json.load(server)
        return jsonServerData


def getSystemConfig():
    with open(getpath("system.json"), "r") as system:
        jsonSystemData = json.load(system)
        return jsonSystemData


def getBrokerAppConfig():
    with open(getpath("brokers.json"), "r") as brokerapp:
        jsonUserData = json.load(brokerapp)
        for broker in jsonUserData["brokers"]:
            if broker["selected"] == True:
                return broker
        return None


def getHolidays():
    with open(getpath("holidays.json"), "r") as holidays:
        holidaysData = json.load(holidays)
        return holidaysData


def getTimestampsData():
    serverConfig = getServerConfig()
    timestampsFilePath = os.path.join(serverConfig["deployDir"], "timestamps.json")
    if os.path.exists(timestampsFilePath) == False:
        return {}
    timestampsFile = open(timestampsFilePath, "r")
    timestamps = json.loads(timestampsFile.read())
    return timestamps


def saveTimestampsData(timestamps={}):
    serverConfig = getServerConfig()
    timestampsFilePath = os.path.join(serverConfig["deployDir"], "timestamps.json")
    with open(timestampsFilePath, "w") as timestampsFile:
        json.dump(timestamps, timestampsFile, indent=2)
    print("saved timestamps data to file " + timestampsFilePath)
