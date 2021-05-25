# ProximityAlert
# Table of Contents
* [Description Table](#Description-Table)
* [How it works](#How-it-works)
* [1. Azure Setup](#1.Azure-Setup)
     1. [Prerequisites](#Prerequisites)
     2. [Deployment](#Deployment)
* [2. Raspberry Pi Setup](#2.Raspberry-Pi-Setup)
     1. [Prerequisites](#Prerequisites-1)
     2. [Deployment](#Deployment-1)
* [Deployment](#Deployment)

## Description Table
File Name | Description
------------ | -------------
ProximityAlert_D2C.py | Python file on Raspberry Pi used to detect cars and send alerts to IoT hub. 
azure.ProximityAlert-Infra-deploy.json | Arm template
setup.bat | Batch file
setup.sh | Shell script

## How it works
There are two parts to this setup,
1. Azure Setup
2. Raspberry Pi Setup 

## 1.Azure Setup
### Prerequisites
* An installed and configured Azure CLI

__*Note*__: *Ensure you have logged in through Azure CLI using `az login` before running the below scripts.*

### Deployment
This setup can deployed on either __Windows Environment__ (using `setup.bat`) or __Linux Environment__ (using `setup.sh`).

The setup file creates a new Resource group and then deploys the Resources to it. The Following resources are created:
1. Service Bus Namespace
2. Service Bus Queue
3. IoT Hub
4. Logic App 
5. Logic App Connectors

#### On Windows Environment
In command prompt run ```setup.bat```
##### Example:
```
   >setup.bat
   Starting...
   Enter resource group name: <Insert Resource Group Name>
```
#### On Linux Environment
In terminal run ```setup.sh```

##### Example:
```
   $setup.sh
   Starting...
   Enter resource group name: <Insert Resource Group Name>
```
## 2.Raspberry Pi Setup
### Prerequisites
* Pre-configured Raspberry Pi with Python.
* Primary Connection String from Azure IoT-Hub. 

### Deployment
First, We need to create an IoT Device in the IoT Hub. In the Azure portal, navigate to IoT Hub -> IoT Devices -> +New. Provide the Device ID and let the other parameters be default. We will later use the primary connection string of this IoT Device.

Next, We have to install an Azure IoT Package. To do this open the Raspberry Pi Terminal and run `sudo pip3 install azure-iot-device`.

Create a python file and copy the contents of `ProximityAlert_D2C.py` in it. Replace the `CONNECTION_STRING = "<Your-Primary-Connection-String>"` with primary connection string obtained from IoT Hub.

To start the setup, run it using `sudo python3 <file-name>.py`.
