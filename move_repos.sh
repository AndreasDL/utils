#! /bin/bash
set -e

function moveImage(){
    from_registery=$1
    to_registery=$2
    name=$3

    az acr login --name ${from_registery}
    docker pull  ${from_registery}/${name}
    docker tag  ${from_registery}/${name} ${to_registery}/${name}

    az acr login --name ${to_registery}
    docker push ${to_registery}/${name}
}

moveImage "from" "to" "image_name"
