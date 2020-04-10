#!/usr/bin/env bash

echo "Downloading DICOMs"
# If not on GCP need to download this
$HOME/gsutil/gsutil cp gs://covid-dicoms/covid-dicoms.tar.gz /data/covid-dicoms.tar.gz
$HOME/gsutil/gsutil cp gs://covid-dicoms/PREM-20090113.zip /data/PREM-20090113.zip


# But in my walled garden, this should work
#wget https://console.cloud.google.com/storage/browser/covid-dicoms/covid-dicoms.tar.gz
echo "Success, unzipping."
tar -xzf /data/covid-dicoms.tar.gz -C /data
unzip PREM-20090113.zip

python /program.py


