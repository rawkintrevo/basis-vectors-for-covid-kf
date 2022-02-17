#!/usr/bin/env bash

image_name=rawkintrevo/covid-basis-vectors # Specify the image name here
image_tag=0.2.1
full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")"
docker build -t "${full_image_name}" .
docker push "$full_image_name"
