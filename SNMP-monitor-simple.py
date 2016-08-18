import csv
import subprocess
#import _thread

def GetPostData(community, target, OID):
    result = subprocess.check_output(["snmpget", "-v", "2c","-c",community,target,OID,"-Ov"])
    # substring the result
    return result

def PostData (targetInflux, host, target, sensor, value):
    postData = subprocess.check_output(["curl", "-i", "-XPOST","http://"+targetInflux+":8086/write?db=home","--data-binary",host + ",host="+ target +",sensor="+sensor+" value=" + value])
    return

def Process(targetInflux,host,target,sensor,community,OID):
    value = GetPostData(community,target,OID)
    PostData(targetInflux,host,sensor,value)
    return

#def threaded_GetPostData(self, targetInflux):
#    _thread.start_new_thread(self.GetData(self, targetInflux))
#    return

def importCSV ():
    input_file = csv.DictReader(open("D:\Python\MonitorScript\data.csv"))
    return input_file

def main():
    influxDB = "dockerhost.ldc.int"
    csvData = importCSV()
    for item in csvData:
        Process(influxDB,item['host'],item['target'],item['sensor'],item['community'],item['OID'])

if __name__ == "__main__":
    main()

