set -e

TAG="docker-tag"
REGISTERY="registery.azurecr.io"
REGISTERY_USERNAME="registry"
RESOURCE_GROUP="resource-group"

docker build -t $TAG .
docker tag $TAG $REGISTERY/$TAG:latest

az acr login --name $REGISTERY 
docker push ${REGISTERY}/${TAG}:latest

echo "get registery password of the containerRegistery / Access keys"
az container create \
    --resource-group $RESOURCE_GROUP \
    --name $TAG \
    --image ${REGISTERY}/${TAG}:latest \
    --registry-username $REGISTERY_USERNAME \
    --restart-policy OnFailure \
    --dns-name-label $TAG \
    --ports 80 \
    --memory 16 \
    --cpu 4

az container restart \
    --resource-group $RESOURCE_GROUP \
    --name $TAG
