#!/bin/bash

# Config
APP_NAME="crc-function-pyglobal"
RESOURCE_GROUP="rg-cloud-resume"
STORAGE_ACCOUNT="crcfunctpystorage"
LOCATION="eastus"
APPSETTINGS_FILE="appsettings.json"

echo "🚀 Creating Azure Function App: $APP_NAME"
az functionapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --storage-account $STORAGE_ACCOUNT \
  --consumption-plan-location $LOCATION \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --os-type Linux \
  --tags department=Development

echo "⏳ Waiting 90 seconds for Kudu provisioning..."
sleep 90

echo "📦 Deploying app settings via ARM template..."
az deployment group create \
  --name appsettings-deploy-$APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --template-file $APPSETTINGS_FILE

echo "🚀 Publishing function using Core Tools..."
func azure functionapp publish $APP_NAME --python

echo "✅ Deployment complete!"
echo "Test your function at:"
echo "  https://$APP_NAME.azurewebsites.net/api/VisitorCounter"
