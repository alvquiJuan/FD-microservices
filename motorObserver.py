import paho.mqtt.client as mqtt
import json
import time



def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.publish("status","ready",2)
       # client_connected=True
        client.subscribe("thermal/sensor")
    else:
        print("something wrong happened ", rc)

    

def on_message(client, userdata, message):
    theMessage=json.loads(message.payload.decode("utf-8"))
    theVal=theMessage["message"]["Value"]
   
       
    print('message received ',theVal)

# print('sleeping')
# time.sleep(5)
print('starting client')
client = mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message

print('starting connection')
client.connect_async('mqtt', 1883, 60)
print('loop start')  
client.loop_start()

while True:
    time.sleep(0.05)
