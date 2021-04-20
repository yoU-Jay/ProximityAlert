@ECHO OFF

ECHO Starting...
set /p rg=Enter resource group name:

call az group create --name %rg% --location eastus
call az deployment group create --resource-group %rg% --template-file azure.ProximityAlert-Infra-deploy.json

ECHO DONE!