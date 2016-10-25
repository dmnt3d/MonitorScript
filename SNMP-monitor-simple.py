import csv
import subprocess
import re
import logging
import time
<<<<<<< HEAD
import requests
from logging.handlers import RotatingFileHandler

#SET FORMATTING for LOG
#logFilename = "SNMP-monitor.log"
logFilename = "/home/admin/Scripts/Python/MonitorScript/log/SNMP-monitor.log"
=======

from logging.handlers import RotatingFileHandler

#SET FORMATTING for LOG
logFilename = "SNMP-monitor.log"
# logFilename = "/home/admin/Scripts/Python/MonitorScript/log/SNMP-monitor.log"
>>>>>>> 065e186a442c9f36b4fc165c03fb53aa580a749d

formatter = logging.Formatter("%(asctime)s[%(levelname)s]: %(message)s")
handler = RotatingFileHandler(logFilename, maxBytes=104800, backupCount=5)
#

#set formatting for the handling
handler.setFormatter(formatter)

# create Logger
logger  = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)




def GetPostData(community, target, OID, table):
    logger.debug("Getting Post Data via SNMPGet")
    result = subprocess.check_output(["snmpget", "-v", "2c","-c",community,target,OID,"-Ov"])
    result = re.findall("[-+]?\d+[\.]?\d*", result)
    # substring the result
    #CHECK if PAN PORTS or NOT
    if (table == "pan_ports"):
        return result[1]
    else:
        return result[0]

def PostData (targetInflux, table, target, sensor, value):
<<<<<<< HEAD
    logger.debug("Posting data for : [" +target+"]")
    while True:
        try:
            # try posting data
        logger.debug("PostCMD: curl -i -XPOST http://"+targetInflux+":8086/write?db=home --data-binary '"+ table +",host="+ target +",sensor="+sensor+" value=" + value + "'")
           # postData = subprocess.check_output(["curl", "-i", "-XPOST","http://"+targetInflux+":8086/write?db=home","--data-binary",  "'" + table +",host="+ target +",sensor="+sensor+" value=" + value +  "'"])
    data  =  table +",host="+ target +",sensor="+sensor+" value=" + value
	    response = requests.post ("http:///"+targetInflux+":8086/write?db=home",data)
	    logger.debug("Done Posting")
	    if (response  == "<Response [204]>"):
	         break
            else:
#        except data as e:
                 logger.debug("FAILED posting. Retrying after 30 seconds... ")
                 time.sleep(30)
                 continue
#        break

    logger.debug ("Continue execution")
=======
    logger.debug("Posting data")
    while True:
        try:
            # try posting data
            postData = subprocess.check_output(["curl", "-i", "-XPOST","http://"+targetInflux+":8086/write?db=home","--data-binary",  table +",host="+ target +",sensor="+sensor+" value=" + value])
        except subprocess.CalledProcessError as e:
            logger.debug("FAILED posting with error: "  +  e.output)
            logger.debug("Retrying after 30 seconds... ")
            time.sleep(30)
            continue
        break

>>>>>>> 065e186a442c9f36b4fc165c03fb53aa580a749d
    return

def Process(targetInflux,table,target,sensor,community,OID):
    value = GetPostData(community,target,OID,table)
<<<<<<< HEAD
    logger.debug("Adding: [" + sensor + "] with VALUE: [" + value + "]")
=======
    logger.debug("Adding: " + sensor + " with VALUE: " + value)
>>>>>>> 065e186a442c9f36b4fc165c03fb53aa580a749d
    #print ("Adding: " + sensor + " with VALUE: " + value)
    PostData(targetInflux,table,target,sensor,value)
    return

#def threaded_GetPostData(self, targetInflux):
#    _thread.start_new_thread(self.GetData(self, targetInflux))
#    return

def importCSV ():
    logger.debug("Importing the CSV data")
<<<<<<< HEAD
#    input_file = csv.DictReader(open("D:\Python\MonitorScript\data.csv"))
    input_file = csv.DictReader(open("/home/admin/Scripts/Python/MonitorScript/data.csv"))
=======
    input_file = csv.DictReader(open("D:\Python\MonitorScript\data.csv"))
#   input_file = csv.DictReader(open("/home/admin/Scripts/Python/MonitorScript/data.csv"))
>>>>>>> 065e186a442c9f36b4fc165c03fb53aa580a749d

    return input_file

def mainLoop (csvData, influxDB):
     for item in csvData:
        Process(influxDB,item['table'],item['target'],item['sensor'],item['community'],item['OID'])


def main():
    influxDB = "dockerhost.ldc.int"
<<<<<<< HEAD
    #csvData = importCSV()
    while True:
	csvData = importCSV()
        mainLoop(csvData, influxDB)
	logger.debug ("Preparing for next execution cycle after 30 secs")
        time.sleep(30)
	logger.debug ("Executing next Cycle")
	
	
=======
    csvData = importCSV()
    while True:
        mainLoop(csvData, influxDB)
        time.sleep(30)

>>>>>>> 065e186a442c9f36b4fc165c03fb53aa580a749d

if __name__ == "__main__":
    logger.debug("Starting Application")
    main()

