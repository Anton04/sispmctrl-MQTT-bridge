sispmctl-MQTT-bridge
=====================

This code implement the function of controlling Gembird silverlit USB switchable outlets through MQTT


The script will need you to install sispmctl

On Ubuntu/RPI use:
sudo apt-get install sispmctl

How to use: 

The command 

>mosquitto_pub -h brokerIP -t "sispmcltr/DEVICE_SERIAL/OUTLET/set" -m On

Will turn on outlet OUTLET (numbered 1-4) on the gembird device with the serial DEVICE_SERIAL. 

To get the ids run: 
>sispmctl -s  

The script will also write a 

sispmcltr/01:1c:aa:b5:41/connected True

When a device is detected or False when disconnected. 

