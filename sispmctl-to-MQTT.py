#!/usr/bin/python

import mosquitto,sys
import json
import thread
import time
import sys
import os

#The MQTT format for setting outlets are PREFIX/DEVICE_ID/OUTLET/set 

PREFIX = "sispmcltr"
MQTT_HOST = "localhost"
POLL_TIME = 5 #For checking state changes on outlets. 


def socket_off(device,socket):
    #print "turn socket",num,"off"
    #print "/usr/local/bin/sispmctl -f "+str(num)
    os.system("/usr/bin/sispmctl -q -d %i -f %i" %(device,socket))

def socket_on(device,socket):
    #print "turn socket",num,"on"
    os.system("/usr/bin/sispmctl -q -d %i -o %i" %(device,socket))
    

def socket_get_state(num):
    #print "get state of socket",num
    #fd=os.popen("/usr/local/bin/sispmctl -g "+str(num))
    result=[]
    for line in os.popen("/usr/bin/sispmctl -q -d %s -n -g all" % str(num)).readlines():
        #print "line: ",line       
        if line[0]=="0":
            result.append(0)
        elif line[0]=="1":
            result.append(1)
    return result
    
def socket_get_serialnumbers():
    #print "get state of socket",num
    #fd=os.popen("/usr/local/bin/sispmctl -g "+str(num))
    Devices = {}
    for line in os.popen("/usr/bin/sispmctl -s ").readlines():
        #print "line: ",line       
        if line.find("serial number") != -1:
            Serial = line.strip("\n").split("    ")[1]
            Devices[Serial]=len(Devices)
            
    return Devices

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
    	    value = msg.payload
    	    if not topics[-3] in devices:
    	        return

    	    #print topics 
	    #print value
 
    	    device = devices[topics[-3]]
    	    socket = int(topics[-2])
    	    
    	    if value.upper()== "ON" or value == "1":
    	        #Turn on
    	        socket_on(device,socket)
    	    else:
    	        #Turn off
    	        socket_off(device,socket)
    	    
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


    


client = mosquitto.Mosquitto("sispmctl-to-MQTT-client")


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
    old_devices = devices
    devices = socket_get_serialnumbers()
    
    #Look for disconnections..
    for device in old_devices:
        if not device in devices:
            topic = PREFIX +"/"+ device + "/connected"
            client.publish(topic , False, 1)
            
    #Look for devices being connected..
    for device in devices:
        if not device in old_devices:
            topic = PREFIX +"/"+ device + "/connected"
            client.publish(topic , True, 1)
            
    #Detect states changes on outlets
    #for device in devices:
        
    
    time.sleep(POLL_TIME)    
       
    
    
client.disconnect() 
