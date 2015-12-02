#!/bin/sh env

if [ ! -d "/data/db/" ]; then
    sudo mkdir -p /data/db/
    echo "Info: create directory /data/db/"
fi

service mongod stop
mongod --dbpath=/data/db/