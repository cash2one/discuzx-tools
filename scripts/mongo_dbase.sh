#!/bin/sh env

if [ ! -d "/data/db/mongodb/" ]; then
    sudo mkdir -pv /data/db/mongodb/
fi

# service mongod stop
nohup mongod --config ../conf/mongod.conf &
