import csv
import subprocess
import re
import logging
import time

from logging.handlers import RotatingFileHandler

#import _thread

logFilename = "SNMP-monitor.log"
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

logger  = logging.getLogger()

handler = RotatingFileHandler(logFilename, maxBytes=100, backupCount=5)
logger.addHandler(handler)

logger.debug("Starting Application")


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
    logger.debug("Posting data")
    postData = subprocess.check_output(["curl", "-i", "-XPOST","http://"+targetInflux+":8086/write?db=home","--data-binary",  table +",host="+ target +",sensor="+sensor+" value=" + value])
    return

def Process(targetInflux,table,target,sensor,community,OID):

    value = GetPostData(community,target,OID,table)
    #print ("Adding: " + sensor + " with VALUE: " + value)
    PostData(targetInflux,table,target,sensor,value)
    return

#def threaded_GetPostData(self, targetInflux):
#    _thread.start_new_thread(self.GetData(self, targetInflux))
#    return

def importCSV ():
    input_file = csv.DictReader(open("D:\Python\MonitorScript\data.csv"))
    return input_file

def main():
    influxDB = "dockerhost.ldc.int"
    logger.debug("Importing CSV Data")
    csvData = importCSV()
    for item in csvData:
        Process(influxDB,item['table'],item['target'],item['sensor'],item['community'],item['OID'])

if __name__ == "__main__":
    main()

