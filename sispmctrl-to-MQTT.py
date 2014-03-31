from RFXtrx.pyserial import PySerialTransport
from RFXtrx import LightingDevice
import mosquitto,sys
import json
import thread
import time
from RFXtrx.lowlevel import Lighting2 


PREFIX = "sispmcltr"
MQTT_HOST = "localhost"

def on_connect(mosq, rc,a):
    mosq.subscribe(PREFIX+"/#", 0)

def on_message(a,mosq, msg):
    global transport
    #try:
    if True:
    	print("RECIEVED MQTT MESSAGE: "+msg.topic + " " + str(msg.payload))
    	topics = msg.topic.split("/")
    	name = topics[-2]
    	if topics[-1] == "set":
    	    value = int(msg.payload)
    	    #print "Set command"

    #Here the control code will go...	    
    
    return 
    
def ControlLoop():
    # schedule the client loop to handle messages, etc.
    print "Starting MQTT listener"
    while True:
        client.loop()
        time.sleep(0.1)

transport = PySerialTransport(PORT, debug=True)
#transport.reset()
client = mosquitto.Mosquitto("RFXcom-to-MQTT-client")


#Connect and notify others of our presence. 
client.connect(MQTT_HOST)
client.publish("system/sispmctrl-to-MQTT", "Online",1)
client.on_connect = on_connect
client.on_message = on_message

#Start tread...
thread.start_new_thread(ControlLoop,())

while True:
   #Check if anything changed
   #Send update if it did. 
   time.sleep(2)
   
    
    
client.disconnect() 
