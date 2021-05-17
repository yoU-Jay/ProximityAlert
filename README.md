# ProximityAlert
# Table of Contents
1. [Prerequisites](#Prerequisites)
2. [Deployment](#Deployment)
3. [Description Table](#Description-Table)

## Prerequisites
* An installed and configured Azure CLI

## Deployment
__*Note*__: *Ensure you have logged in to Azure CLI using `az login` before running the below scripts.*

### On Windows Environment
In command prompt run ```setup.bat```
#### Example:
```
   >setup.bat
   Starting...
   Enter resource group name: <Insert Resource Group Name>
```
### On Linux Environment
In terminal run ```setup.sh```

#### Example:
```
   $setup.sh
   Starting...
   Enter resource group name: <Insert Resource Group Name>
```

## Description Table
File Name | Description
------------ | -------------
ProximityAlert_D2C.py | Python file on Raspberry Pi used to detect cars and send alerts to IoT hub. 
azure.ProximityAlert-Infra-deploy.json | Arm template
setup.bat | Batch file
setup.sh | Shell script
