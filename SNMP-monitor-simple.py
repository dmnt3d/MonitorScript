import csv
import subprocess
import re
import logging
import time
import requests
from logging.handlers import RotatingFileHandler

# SET FORMATTING for LOG
#logFilename = "SNMP-monitor.log"
logFilename = "/home/admin/Scripts/Python/MonitorScript/log/SNMP-monitor.log"

formatter = logging.Formatter("%(asctime)s[%(levelname)s]: %(message)s")
handler = RotatingFileHandler(logFilename, maxBytes=104800, backupCount=5)
#

#set formatting for the handling
handler.setFormatter(formatter)

# create Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def GetPostData(community, target, OID, table):
    logger.debug("Getting Post Data via SNMPGet")
    result = subprocess.check_output(["snmpget", "-v", "2c", "-c", community, target, OID, "-Ov"])
    result = re.findall("[-+]?\d+[\.]?\d*", result)
    # substring the result
    #CHECK if PAN PORTS or NOT
    if ("ports" in table):
        return result[1]
    else:
        return result[0]


def PostData(targetInflux, table, target, sensor, value):
    logger.debug("Posting data for : [" + target + "]")
    while True:
        logger.debug("PostCMD: curl -i -XPOST http://" + targetInflux + ":8086/write?db=home --data-binary '" + table + ",host=" + target + ",sensor=" + sensor + " value=" + value + "'")
        # postData = subprocess.check_output(["curl", "-i", "-XPOST","http://"+targetInflux+":8086/write?db=home","--data-binary",  "'" + table +",host="+ target +",sensor="+sensor+" value=" + value +  "'"])
        data = table + ",host=" + target + ",sensor=" + sensor + " value=" + value
        response = requests.post("http://" + targetInflux + ":8086/write?db=home", data)

        if (response.status_code == 204):
            logger.debug("Done Posting")
            break
        else:
            logger.debug("FAILED posting. Retrying after 30 seconds... ")
            time.sleep(30)
            continue
    logger.debug("Continue execution")
    return


def Process(targetInflux, table, target, sensor, community, OID):
    value = GetPostData(community, target, OID, table)
    logger.debug("Adding: [" + sensor + "] with VALUE: [" + value + "]")
    #print ("Adding: " + sensor + " with VALUE: " + value)
    PostData(targetInflux, table, target, sensor, value)
    return


#def threaded_GetPostData(self, targetInflux):
#    _thread.start_new_thread(self.GetData(self, targetInflux))
#    return

def importCSV():
    logger.debug("Importing the CSV data")
    #input_file = csv.DictReader(open("D:\Python\MonitorScript\data.csv"))
    input_file = csv.DictReader(open("/home/admin/Scripts/Python/MonitorScript/data.csv"))

    return input_file


def mainLoop(csvData, influxDB):
    for item in csvData:
        Process(influxDB, item['table'], item['target'], item['sensor'], item['community'], item['OID'])


def main():
    influxDB = "dockerhost.ldc.int"
    #csvData = importCSV()
    while True:
        csvData = importCSV()
        mainLoop(csvData, influxDB)
        logger.debug("Preparing for next execution cycle after 30 secs")
        time.sleep(30)
        logger.debug("Executing next Cycle")


if __name__ == "__main__":
    time.sleep(60)
    logger.debug("Starting Application")
    main()

