#!/bin/sh env

if [ ! -d "/data/db/" ]; then
    sudo mkdir -pv /data/db/
fi

service mongod stop
mongod --config mongod.conf
