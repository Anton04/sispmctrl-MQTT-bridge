#!/usr/bin/python

import mosquitto,sys
import json
import thread
import time
import sys
import os
import ConfigParser

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
if __name__ == '__main__':


	#Where am I 
	path = os.path.abspath(os.path.dirname(sys.argv[0]))

	#Load config file... 	

	try:
		ConfigFile = sys.argv[1]
	except:
		ConfigFile = path + "/sispmctrl.conf"

	try:
		f = open(ConfigFile,"r")
		f.close()
	except:
		try:
			ConfigFile = path + "/sispmctrl.conf"
			f = open(ConfigFile,"r")
                	f.close()
		except:
			print "Please provide a valid config file! By argument or as default sispmctrl.conf file."
			exit(1)
	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.read(ConfigFile)


	#Load basic config. 
	ip = config.get("MQTTServer","Address")
	port = config.get("MQTTServer","Port")
	user = config.get("MQTTServer","User")
	password = config.get("MQTTServer","Password")
	prefix = config.get("MQTTServer","Prefix")   


	client = mosquitto.Mosquitto("sispmctl-to-MQTT-client")

	if user != None:
    			client.username_pw_set(user,password)

	client.will_set( topic =  "system/" + prefix, payload="Offline", qos=1, retain=True)

	#Connect and notify others of our presence. 
	client.connect(ip)
	client.publish("system/" + prefix, "Online",1, retain=True)
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
	            topic = prefix +"/"+ device + "/connected"
	            client.publish(topic , False, 1)
	            
	    #Look for devices being connected..
	    for device in devices:
	        if not device in old_devices:
	            topic = prefix +"/"+ device + "/connected"
	            client.publish(topic , True, 1)
	            
	    #Detect states changes on outlets
	    #for device in devices:
	        
	    
	    time.sleep(POLL_TIME)    
	       
	    
	    
	client.disconnect() 
