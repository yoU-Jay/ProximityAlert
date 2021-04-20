#!/bin/bash

echo Starting..

read -p 'Enter resource group name: ' rg
az group create --name $rg --location eastus
az deployment group create --resource-group $rg --template-file azure.ProximityAlert-Infra-deploy.json

echo Done!