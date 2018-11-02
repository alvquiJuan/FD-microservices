import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

'''
Class to evaluate motor damage relevance acording to ATSM E1934-99a

'''
class ThermalRules:
    def __init__(self):
        #universes for input and output data
        #we have 4 antecedents (4 thermal signatures)
        tc1=ctrl.Antecedent(np.arange(0, 45), 'tc1')
        tc2=ctrl.Antecedent(np.arange(0, 45), 'tc2')
        tc3=ctrl.Antecedent(np.arange(0, 45), 'tc3')
        tc4=ctrl.Antecedent(np.arange(0, 45), 'tc4')
        #one consequent (the motor condition)
        condition=ctrl.Consequent(np.arange(101),'condition')

        #membership functions
        #antecedent functions

        tc1['negligible']=fuzz.trapmf(tc1.universe,[0,0,1,2])
        tc1['low']=fuzz.trapmf(tc1.universe,[1,2,4,5])
        tc1['medium']=fuzz.trapmf(tc1.universe,[4,5,14,15])
        tc1['high']=fuzz.trapmf(tc1.universe,[14,15,29,30])
        tc1['extreme']=fuzz.trapmf(tc1.universe,[29,30,45,45])

        tc2['negligible']=fuzz.trapmf(tc2.universe,[0,0,1,2])
        tc2['low']=fuzz.trapmf(tc2.universe,[1,2,4,5])
        tc2['medium']=fuzz.trapmf(tc2.universe,[4,5,14,15])
        tc2['high']=fuzz.trapmf(tc2.universe,[14,15,29,30])
        tc2['extreme']=fuzz.trapmf(tc2.universe,[29,30,45,45])

        tc3['negligible']=fuzz.trapmf(tc3.universe,[0,0,1,2])
        tc3['low']=fuzz.trapmf(tc3.universe,[1,2,4,5])
        tc3['medium']=fuzz.trapmf(tc3.universe,[4,5,14,15])
        tc3['high']=fuzz.trapmf(tc3.universe,[14,15,29,30])
        tc3['extreme']=fuzz.trapmf(tc3.universe,[29,30,45,45])

        tc4['negligible']=fuzz.trapmf(tc4.universe,[0,0,1,2])
        tc4['low']=fuzz.trapmf(tc4.universe,[1,2,4,5])
        tc4['medium']=fuzz.trapmf(tc4.universe,[4,5,14,15])
        tc4['high']=fuzz.trapmf(tc4.universe,[14,15,29,30])
        tc4['extreme']=fuzz.trapmf(tc4.universe,[29,30,45,45])


        #uncomment next line to expose antecedent sets
        tc1.view()


        #consequent functions
        condition['excelent']=fuzz.trapmf(condition.universe,[90,95,100,100])
        condition['ordinary']=fuzz.trapmf(condition.universe,[75,80,90,95])
        condition['slight']=fuzz.trapmf(condition.universe,[60,65,75,80])
        condition['major']=fuzz.trapmf(condition.universe,[35,40,60,65])
        condition['critical']=fuzz.trapmf(condition.universe,[0,0,35,40])
        #uncomment next line to expose consequent sets
##        self.condition=condition

        #fuzzy Rules.
        rules=[None]*8
        rules[0]=ctrl.Rule(tc1['negligible']&tc2['negligible']&tc3['negligible']&tc4['negligible'], condition['excelent'],label='HLT')
        rules[1]=ctrl.Rule(tc1['medium']&tc2['medium']&tc3['medium']&tc4['medium'], condition['ordinary'],label='1/2brb')
        rules[2]=ctrl.Rule(tc1['low']&tc2['low']&tc3['medium']&tc4['low'], condition['slight'],label='1brb')
        rules[3]=ctrl.Rule(tc1['medium']&tc2['low']&tc3['low']&tc4['negligible'], condition['major'],label='2brb')
        rules[4]=ctrl.Rule(tc1['medium']&tc2['medium']&tc3['negligible']&tc4['medium'], condition['slight'],label='bd')
        rules[5]=ctrl.Rule(tc1['medium']&tc2['medium']&tc3['high']&tc4['high'], condition['major'],label='unb')
        rules[6]=ctrl.Rule(tc1['negligible']&tc2['negligible']&tc3['negligible']&tc4['medium'], condition['slight'],label='vunb')
        rules[7]=ctrl.Rule(tc1['extreme']&tc2['high']&tc3['extreme']&tc4['high'], condition['critical'],label='MAL')
        self.motor_ctrl = ctrl.ControlSystem(rules)

        #simulation for the motor condition
        self.motor = ctrl.ControlSystemSimulation(self.motor_ctrl)

    '''
    method for motor evaluation
    the parameters are the thermal coefficient for each component
    '''
    def compute_status(self,pf_tc1,pf_tc2,pf_tc3,pf_tc4):
        processed_tc1=np.clip(pf_tc1,0,45)
        processed_tc2=np.clip(pf_tc2,0,45)
        processed_tc3=np.clip(pf_tc3,0,45)
        processed_tc4=np.clip(pf_tc4,0,45)

        self.motor.input['tc1'] = processed_tc1
        self.motor.input['tc2'] = processed_tc2
        self.motor.input['tc3'] = processed_tc3
        self.motor.input['tc4'] = processed_tc4
        # for rule in self.motor_ctrl.rules:
        #     print(self.motor.compute_rule(rule))
        self.motor.compute()
        return (self.motor.output['condition'])

myThermal=ThermalRules()

##myThermal.condition.view()
#input("press a key to continue...")
print("bearing defect")
for i in range (10):
    temperatures=30*np.random.rand(4)+15
    temperatures[0]=np.clip(temperatures[0],30,45)
    temperatures[1]=np.clip(temperatures[1],15,29)
    temperatures[2]=np.clip(temperatures[2],30,45)
    temperatures[3]=np.clip(temperatures[3],15,29)
    print( myThermal.compute_status(temperatures[0],temperatures[1],temperatures[2],temperatures[3]))
# print('half broken rotor motor status:', myThermal.compute_status(6.03,5.63,4.83,5.33))
# print('one broken rotor motor status:', myThermal.compute_status(3.43,3.07,5.03,3.67))
# print('two broken rotor motor status:', myThermal.compute_status(4.5,2.73,2.87,1.4))
# print('Bearing defect motor status:', myThermal.compute_status(5.3,8.97,0,7.3))
# print('mechanical unbalance motor status:', myThermal.compute_status(8.03,5.95,12.03,9.5))
# print('voltage unbalance motor status:', myThermal.compute_status(0,0,0,6))
# print('Misaligned motor status:', myThermal.compute_status(32.73,28.2,39.77,25.93))
