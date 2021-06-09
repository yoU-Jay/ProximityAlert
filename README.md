# ProximityAlert
ProximityAlert is a parking detection and alerting application built using IoT and Cloud technologies. It aims at automating and simplifying the parking management system. With real-time monitoring, ProximityAlert helps the user stay connected with their vehicles while monitoring their costs and giving them a sense of security.

## Objectives
1. To integrate and setup Ultrasonic sensor with Raspberry Pi.
2. To setup and deploy resources to Azure.
3. To detect vehicles in a parking lot and send email alerts to the user. 

## Description Table
File Name | Description
------------ | -------------
[Setup.md](#Setup.md) | Setup and Deployment Guide
[Design.md](#Design.md) | Design description
ProximityAlert_D2C.py | Python file on Raspberry Pi used to detect cars and send alerts to IoT hub. 
azure.ProximityAlert-Infra-deploy.json | ARM template
setup.bat | Batch file
setup.sh | Shell script
