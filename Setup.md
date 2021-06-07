# Setup guide
---
# Overview
This setup guide deals with setting up and deploying the **ProximityAlert** infrastructure.

# Contents
* [Requirements](#Requirements)
* [Architecture](#Architecture)
* [Setup](#Setup)
  1. [1. Setting up Azure](#1.Setting-up-Azure)
     * [Prerequisites](#Prerequisites)
     * [Deployment](#Deployment)
  2. [2. Setting up Raspberry Pi](#2.Setting-up-Raspberry-Pi)
     * [Before you get started](#Before-you-get-started)
     * [Making the connections](#Making-the-connections)
     * [Inside the Pi](#Inside-the-Pi)
* [Deployment](#Deployment)


# Requirements
Hardware and Software tools required for this setup are listed below.
1. Raspberry Pi 3 Model B+
2. Ultrasonic Distance Sensor Module (HC-SR04)
3. Resistors - 1 x 560 Ω and 1 x 800 Ω
4. Microsoft Azure subscription
5. Azure CLI 


# Architecture
###Add ultrasonic sensor###
![ProximityAlert_infra](https://user-images.githubusercontent.com/59735375/120606670-0f2cb680-c46d-11eb-8e24-33a730d5d494.png)


# Setup
There are two parts to this setup,
1. Azure Setup
2. Raspberry Pi Setup 

## 1.Setting up Azure

* ### Prerequisites
  * An installed and configured Azure CLI

* ### Deployment
  This setup can deployed on either __Windows Environment__ (using `setup.bat`) or __Linux Environment__ (using `setup.sh`).
  
    > __*Note*__  
    > The setup file creates a new Resource group and then deploys the Resources to it. The Following resources are created:
    > 1. Service Bus Namespace
    > 2. Service Bus Queue
    > 3. IoT Hub
    > 4. Logic App 
    > 5. Logic App Connectors
  
  1. Open a **terminal** and login to Azure using `az login` command.
  
  2. Depending on the environment you are using, run the following command:  
      * ##### In Windows Environment
        In command prompt run ```setup.bat```
        ###### Example:
        ```
          >setup.bat
          Starting...
          Enter resource group name: <Insert Resource Group Name>
        ```
      * ##### In Linux Environment
        In terminal run ```setup.sh```
        ###### Example:
        ```
          $setup.sh
          Starting...
          Enter resource group name: <Insert Resource Group Name>
        ```
     This creates a Resource Group in `eastus` and deploys `azure.ProximityAlert-Infra-deploy.json` ARM template in the same Resource Group.
     
  3. An **IoT Device** needs to be created. To do this, in the **Azure Portal**, navigate to the Resource Group created in the previous step.  
  4. Open the **IoT Hub** service.
  5. Click on **IoT devices** under **Explorers**.        
  6. Click on **+New** to add a new IoT device.
  7. Enter a name for your device under **Device ID** and leave other settings as it is.  
  ![image](https://user-images.githubusercontent.com/59735375/121053692-3ff84d00-c7d9-11eb-9757-8eb57f665459.png)
  8. Click on **Save** to save your settings.
  9. After the deployment is complete, Click on your device name under **Device ID** in the IoT Hub page. 
  10. Copy the **Primary Connection String**.  

  

## 2.Setting up Raspberry Pi

* ### Before you get started
  For this setup you need a preconfigured Raspberry Pi with an OS (of your choice) and Python 3 installed. 
  > __*Note*__: This setup was tested with _**Raspberry Pi OS (Raspbian)**_ which has Python 3 pre-installed.

* ### Making the connections
   A HC-SR04 Ultrasonic Distance Sensor Module is used to sense the presence of a vehicle in its proximity. Construct the circuit as shown below.
   
   ![raspberry-pi-hc-sr04-distance-measuring-sensor](https://user-images.githubusercontent.com/59735375/120596889-ec48d500-c461-11eb-96da-7298508035dc.jpg)
   
   ###Explain gpio setup###
  
* ### Inside the Pi
   * Now, after the connections are done, power up your Raspberry Pi. 
   * Open a **Terminal** and create a new directory `Proximity-Alert`
   * Next, We have to install an Azure IoT Package. Inside the newly created directory, run the following command.  
     `sudo pip3 install azure-iot-device`
   * Create a Python file **ProximityAlert_D2C.py** and paste in the following code to setup a Device to Cloud connection. *[How does this code work?](Design.md#Flowchart)*
     > This code reads input from the Ultrasonic sensor module through GPIO Pins, then forms a connection between Raspberry Pi and Azure IoT Hub and transmits the recieved input to Azure.
       ```
       # Libraries
       import RPi.GPIO as GPIO
       import time
       from azure.iot.device import IoTHubDeviceClient, Message
       
       # Primary Connection String
       CONNECTION_STRING = "<Your-Primary-Connection-String>"
       MSG_TXT = '{{"distance":{distance}}}'
       
       # GPIO settings
       GPIO.setmode(GPIO.BCM)
       TRIG = 23
       ECHO = 24
       GPIO.setup(TRIG, GPIO.OUT)
       GPIO.setup(ECHO, GPIO.IN)
       
       # Initiate IoTHub connection
       def iothub_client_init():
           client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
           return client
       
       
       print("Distance Measurement in progress")
       
       #Function to measure distance 
       def distance_measure():
           # try:
         # while True:
       
           GPIO.output(TRIG, False)
           print("Waiting for sensor to settle")
           time.sleep(2)
       
           GPIO.output(TRIG, True)
           time.sleep(0.00001)
           GPIO.output(TRIG, False)
       
           while GPIO.input(ECHO) == 0:
               pulse_start = time.time()
       
           while GPIO.input(ECHO) == 1:
               pulse_end = time.time()
       
           pulse_duration = pulse_end - pulse_start
       
           global distance
       
           distance = pulse_duration * 17150
       
           distance = round(distance, 2)
       
           print("Distance:", distance, "cm")
       
       #Function to check if a parked car moves out of the slot
       def test2():
           while True:
               park_dist_prev = int(distance)
               distance_measure()
               park_dist_curr = int(distance)
               if park_dist_curr != park_dist_prev:
                   print("going to test1")
                   test()
       
       #main
       def test():
           try:
             client = iothub_client_init()
             print("IoT Hub device sending periodic messages, press Ctrl+C to exit")
             while True:
               distance_measure()
               while distance < 20:   ## 20 - max distance of the individual parking lot
                   if distance < 5:   ## 5  - Proximity alert distance
                       msg_txt_formatted = MSG_TXT.format(distance=distance)
                       message = Message(msg_txt_formatted)
                       message.custom_properties["distanceAlert"] = "true"
                       print("YES")
       
                       for property in vars(message).items():
                         if all(property):
                           print("     {0}".format(property))
                       client.send_message(message)
                       print("Message sent")
       
                       prev_dist = int(distance)
                       distance_measure()
                       curr_dist = int(distance)
                       if curr_dist == prev_dist:  
                           for x in range(6):           ##This FOR Loop checks if the car is stationary(parked), by checking if the previous distance is equal to the current distance.
                               print("IN for loop", x)
                               prev_dist = int(distance)
                               distance_measure()
                               curr_dist = int(distance)
                               print("C", curr_dist, "P", prev_dist)
       
                               if curr_dist == prev_dist and x < 5: 
                                   pass
                                   print("pass", x)
       
                               elif x == 5:                         
                                   print("test fn", x)
                                   test2()
       
                               else:                               
                                   print("breaking")
                                   break
                   else:
                       break
           except KeyboardInterrupt:
             print("Cleaning up!")
             GPIO.cleanup()
       
       
       if __name__ == '__main__':
           print("IoT Hub Quickstart ")
           print("ctrlcto exit")
           test()
       ```
   
   * Paste the **Primary Connection String** of the IoT device copied eariler in the `<Your-Primary-Connection-String>` field. 
     Then it would look something like this, 
     ##### Example
     ```
       # Primary Connection String
       CONNECTION_STRING = "HostName=<host-name>.azure-devices.net;DeviceID=<device-id>;SharedAccessKey=.....
     ```
   * Save **ProximityAlert_D2C.py**.

---

# Deployment
