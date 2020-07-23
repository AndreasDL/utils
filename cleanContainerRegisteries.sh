#!/bin/bash
# Delete all untagged (orphaned) images

function cleanRepo(){
    registry=$1
    repository=$2

    az acr repository show-manifests --name "$registry" --repository "$repository"  --query "[?tags[0]==null].digest" -o tsv \
    | xargs -I% az acr repository delete --name "$registry" --image $repository@% --yes
}
function cleanRegistry(){
    registry=$1

    az acr login --name $registry
    for repo in $(az acr repository list --name "$registry" -o tsv);
    do
        echo "cleaning $repo";
        cleanRepo $registry $repo;
    done
}

cleanRegistry ""
