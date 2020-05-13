#!/usr/bin/env bash


# presuming you have a directory `/data` which containes:
# corona CT scans in format `data/case00x/axial/*.dcm
# non-corona CT scans in PCsub*-20090909/*/*/*/*.dcm
# TODO this should be parallelized- could be done so easily.
docker run -v $PWD/data:/data  rawkintrevo/covid-prep-dicom:0.7.12.11 python /program.py --input_dir /data --output_dir /data --min_slice 150 --max_slice 150
# which will write `s.csv` in `data/`

docker run -it -v $PWD/data:/data rawkintrevo/covid-basis-vectors:0.1.9 /opt/spark/bin/spark-submit --master local[*] --class org.rawkintrevo.covid.App /covid-0.1-jar-with-dependencies.jar  244 15 2
# This is actually a full svd. Next regress the original images on basis vectors to determine which basis vectors are least important.


