'''motor simulation'''
from tempObserver import temperatureObserver as to
import csv
csvfile="results.csv"
res=[]

s1=to("Sensor armadura")
s2=to("Sensor rodamiento")
s3=to("Sensor polea de motor")
s4=to("Sensor polea de carga")

'''healthy motor based on García et al Model '''
for iter in range(1000):
    s1.simulateValue(40,45)
    res.append(s1.getValue())
#print(res)

with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(res)
'''
s2.simulateValue(22,50)
s3.simulateValue(22,50)
s4.simulateValue(22,50)
print("====")
print(s1.getReport())
print("====")
print(s2.getReport())
print("====")
print(s3.getReport())
print("====")
print(s4.getReport())
print("====")
'''
