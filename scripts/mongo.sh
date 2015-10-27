#!/bin/sh env

mkdir /data/
mkdir /data/db/

service mongod stop
mongod --dbpath=/data/db/