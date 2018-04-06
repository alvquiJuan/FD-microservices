'''
tempertaure observer class
Author Juan M ÁLvarez
created on: 2018-04-05

'''
import numpy as np
import uuid
import datetime as dt
import json

class temperatureObserver :
    '''
    constructor initializes instance variables
    value stores the temperature last measured (or simulated variable)
    uid stores an unique identifier for the sensor
    '''
    def __init__(self, psname):
        self.uid=uuid.uuid4() #generates a random uuid for the sensor
        self.value=0.0
        self.measureTime=dt.datetime.today()
        self.name=psname
    '''
    value setter
    '''
    def setValue(self,pfval):
        self.value=float(pfval)
        self.measureTime=dt.datetime.today()
    '''
    value getter
    '''
    def getValue(self):
        return float(self.value)
    
    '''
    simulateValue method is used for simulations (i.e. tests)
    '''
    def simulateValue(self,pflow,pfhig):
        #if somebody puts 
        if pflow>pfhig:
            tmp=pflow
            pflow=pfhig
            pfhig=tmp
        
        self.setValue((pfhig-pflow) * np.random.random_sample() + pflow)
        return self.getValue()
    '''
    method for report generation
    compatible with SNON 2.0
    '''
    def getReport(self):
        report={}
        report['messageID']=str(uuid.uuid4()) #message uuid
        report['messageTime']=str(dt.datetime.today().isoformat())
        message={}
        message["entityID"]=str(self.uid)
        message["entityName"]=self.name
        message["entityType"]={"en":"temperature Sensor","es":"sensor de temperatura"}
        message["measureUnit"]="Celsius"
        message["valueTime"]=str(self.measureTime.isoformat())
        message["Value"]=self.getValue()
        report["message"]=message
        return json.dumps(report)
        
        
        
