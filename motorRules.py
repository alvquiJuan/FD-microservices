import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

'''
Class to evaluate motor damage relevance acording to ATSM E1934-99a

'''
class ThermalRules:
    def __init__(self):
        #universes for input and output data
        tc=ctrl.Antecedent(np.arange(0, 45), 'Thermal coefficient')
        condition=ctrl.Consequent(np.arange(101),'component condition')
        #membership functions
        #antecedent functions
        tc["negligible"]=fuzz.trapmf(tc.universe,[0,0,1,2])
        tc["low"]=fuzz.trapmf(tc.universe,[1,2,4,5])
        tc["medium"]=fuzz.trapmf(tc.universe,[4,5,14,15])
        tc["high"]=fuzz.trapmf(tc.universe,[14,15,29,30])
        tc["extreme"]=fuzz.trapmf(tc.universe,[29,30,45,45])
        #uncomment next line to expose antecedent sets 
        #self.tc=tc

        #consequent rules
        condition["excelent"]=fuzz.trapmf(condition.universe,[90,95,100,100])
        condition["ordinary"]=fuzz.trapmf(condition.universe,[75,80,90,95])
        condition["slight"]=fuzz.trapmf(condition.universe,[60,65,75,80])
        condition["major"]=fuzz.trapmf(condition.universe,[35,40,60,65])
        condition["critical"]=fuzz.trapmf(condition.universe,[0,0,35,40])
        #uncomment next line to expose consequent sets 
        #self.condition=condition
        
        
