import sispm
import mosquitto,sys
import json
import thread
import time

#The MQTT format for setting outlets are PREFIX/DEVICE_ID/OUTLET/set 

PREFIX = "sispmcltr"
MQTT_HOST = "localhost"
POLL_TIME = 5 #For checking state changes on outlets. 

def on_connect(mosq, rc,a):
    mosq.subscribe(PREFIX+"/#", 0)

def on_message(a,mosq, msg):
    global devices
    #try:
    if True:
    	print("RECIEVED MQTT MESSAGE: "+msg.topic + " " + str(msg.payload))
    	topics = msg.topic.split("/")
    	name = topics[-2]
    	if topics[-1] == "set":
    	    value = int(msg.payload)
    	    if not topics[-3] in devices:
    	        return
    	    
    	    devices[topics[-3]].set_outlet_enabled(int(topic[-2]),bool(value))
    	    
    #except:
    #   print "Error occured while processing command"
    return 
    
def ControlLoop():
    # schedule the client loop to handle messages, etc.
    print "Starting MQTT listener"
    while True:
        client.loop()
        time.sleep(0.1)


#Get all devices.


    


client = mosquitto.Mosquitto("RFXcom-to-MQTT-client")


#Connect and notify others of our presence. 
client.connect(MQTT_HOST)
client.publish("system/sispmctrl-to-MQTT", "Online",1)
client.on_connect = on_connect
client.on_message = on_message

#Init

devices = {}
states = {}

#Start tread...
thread.start_new_thread(ControlLoop,())

while True:
   #Check if anything changed
   #Send update if it did. 
    
    #Detect devices
    n = sispm.get_num_devices()
    
    for f in range (0,n):
        dev=sispm.Sispm(f)
        filename = dev.device.filename
        
        if not filename in devices:
            devices[filename] = dev
            states[filename] = [None,None,None,None]
            #publish
            topic = PREFIX +"/"+ filename 
            client.publish(topic , "Detected", 1)
    
    #Detect states changes on outlets
    
    
    time.sleep(POLL_TIME)    
       
    
    
client.disconnect() 
